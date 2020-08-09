from abc import ABC, abstractmethod
from copy import deepcopy
from datetime import datetime
from typing import List

from networkx import DiGraph

from tinypy.geometry.intersections import Intersections
from tinypy.geometry.region import Region
from tinypy.polytopes.base_polytope import Polytope
from tinypy.utils.file import create_directory, file_exists, get_full_path


class Tree(ABC):
    """Base class that generates the decisions trees for different polytopes.

    Attributes:
        graph: The graph representation for the tree.
        polytope: The given polytope.
        intersections: Computes the intersections of hyperplanes and cones.
        queue: List of node indices to explore.
        next_node: Index of next node assignable.
        height: Current tree height.
        root: Index of root node.
    """

    graph: DiGraph
    polytope: Polytope
    intersections: Intersections
    tree_file: str

    queue: List[int]
    next_node: int
    height: int
    root: int

    def __init__(self, polytope: Polytope, bfs=False):
        """Initializes the tree.

        Args:
            polytope: The given polytope.
        """
        self.graph = DiGraph()
        self.polytope = polytope
        self.intersections = Intersections(polytope)
        self.queue = []
        self.next_node = 0
        self.height = 0
        self.root = 1
        self.tree_file = get_full_path('files', 'trees', self.polytope.instance.type, f'{self.polytope.instance.name}.tptf')
        create_directory(get_full_path('files', 'trees', self.polytope.instance.type))

        if file_exists(self.tree_file):
            self.graph = self.__read_tree_file()
        else:
            self.__make_tree(bfs)
            self.__write_tree_file()
            self.intersections.clear_files()

    def __make_tree(self, bfs=False):
        """Constructs the tree.

        Args:
            bfs: Whether should use a breadth first or depth first approach.
        """
        root_node = self.__add_node(0, list(self.polytope.vertices.keys()), Region())
        self.queue.append(root_node)
        self.__explore(bfs)

    def __explore(self, bfs: bool = False):
        """Explores each node.

        Args:
            bfs: Whether should use a breadth first or depth first approach.
        """
        height: int
        solutions: List[int]
        hyperplanes: List[int]
        region: Region

        while len(self.queue) > 0:
            if bfs:
                parent_node = self.queue.pop(0)
            else:
                parent_node = self.queue.pop()

            node = self.graph.nodes[parent_node]
            height, solutions, region = node['height'], node['solutions'].copy(), deepcopy(node['region'])
            hyperplane = self.select_hyperplane(solutions)
            node['hyperplane'] = hyperplane
            positions = self.intersections.get_positions(region, solutions, [hyperplane])

            left_solutions = [item for item in solutions if item not in positions[hyperplane].right]
            right_solutions = [item for item in solutions if item not in positions[hyperplane].left]

            left_region = deepcopy(region)
            right_region = deepcopy(region)
            left_region.add_hyperplane(-hyperplane)
            right_region.add_hyperplane(hyperplane)

            left_node = self.__add_node(height + 1, left_solutions, left_region)
            self.graph.add_edge(parent_node, left_node, direction='left')

            if len(left_solutions) > 1:
                self.queue.append(left_node)

            right_node = self.__add_node(height + 1, right_solutions, right_region)
            self.graph.add_edge(parent_node, right_node, direction='right')

            if len(right_solutions) > 1:
                self.queue.append(right_node)

    @abstractmethod
    def select_hyperplane(self, solutions: List[int]) -> int:  # pragma: no cover
        """Selects the next hyperplane given the possible solutions.

        Args:
            solutions: The list of possible solution indices.

        Returns:
            Index of the next hyperplane.
        """
        pass

    def __add_node(self, height: int, solutions: List[int], region: Region) -> int:
        """Adds a node to the tree and updates its height.

        Args:
            height: Node height.
            solutions: Node solutions.
            region: Node region.

        Returns:
            Index of the inserted node.
        """
        self.graph.add_node(self.__get_next_node(), height=height, solutions=solutions, region=region)
        self.height = max(self.height, height)

        return self.next_node

    def __get_next_node(self):
        """Increments and returns the next node.
        """
        self.next_node = self.next_node + 1
        return self.next_node

    def __read_tree_file(self) -> DiGraph:
        graph = DiGraph()

        with open(self.tree_file, 'r') as file:
            file.readline()  # name
            file.readline()  # type
            file.readline()  # generated
            file.readline()  # dimension
            file.readline()  # solutions
            file.readline()  # hyperplanes
            nodes = int(file.readline().split()[1])
            edges = int(file.readline().split()[1])
            self.height = int(file.readline().split()[1])
            file.readline()

            file.readline()  # NODES SECTION
            for _ in range(nodes):
                line = file.readline().split()
                index = int(line[0])
                height = int(line[1])
                hyperplane = int(line[2])
                solutions = list(map(int, file.readline().split()))
                region = list(map(int, file.readline().split()))
                graph.add_node(index, height=height, solutions=solutions, region=Region(region))

                if hyperplane != 0:
                    graph.nodes[index]['hyperplane'] = hyperplane

            file.readline()

            file.readline()  # EDGES SECTION
            for _ in range(edges):
                line = file.readline().split()
                first = int(line[0])
                second = int(line[1])
                direction = line[2]
                graph.add_edge(first, second, direction=direction)

        return graph

    def __write_tree_file(self):
        """Writes the tree graph to a file.
        """
        now = datetime.now()

        with open(self.tree_file, 'w+') as file:
            file.write(f'NAME: {self.polytope.instance.name}\n')
            file.write(f'TYPE: {self.polytope.instance.type.upper()}\n')
            file.write(f'GENERATED: {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
            file.write(f'DIMENSION: {self.polytope.dimension}\n')
            file.write(f'SOLUTIONS: {self.polytope.size}\n')
            file.write(f'HYPERPLANES: {len(self.polytope.H)}\n')
            file.write(f'NODES: {len(self.graph.nodes)}\n')
            file.write(f'EDGES: {len(self.graph.edges)}\n')
            file.write(f'HEIGHT: {self.height}\n\n')

            file.write(f'NODES SECTION\n')
            for index in self.graph.nodes:
                node = self.graph.nodes[index]
                height = node['height']
                hyperplane = node['hyperplane'] if 'hyperplane' in node.keys() else 0
                solutions = node['solutions']
                region = node['region']
                file.write(f'{index} {height} {hyperplane}\n')
                file.write(f'{" ".join(map(str, solutions))}\n')
                file.write(f'{" ".join(map(str, region.hyperplanes))}\n')
            file.write('\n')

            file.write(f'EDGES SECTION\n')
            for edge in self.graph.edges.data():
                file.write(f'{edge[0]} {edge[1]} {edge[2]["direction"]}\n')

