from copy import deepcopy
from math import ceil, log2
from typing import List, Tuple

from networkx import DiGraph
from colorama import Fore, Style


from tinypy.geometry.intersections import Intersections
from tinypy.geometry.region import Region
from tinypy.polytopes.base_polytope import Polytope
from tinypy.models.subtree import Subtree
from tinypy.utils.constants import INFINITY


class DPTree:

    name: str
    type: str
    graph: DiGraph
    polytope: Polytope
    intersections: Intersections
    height: int

    queue: List[Tuple[int, Subtree]]
    next_node: int
    root: int
    height: int

    def __init__(self, polytope: Polytope):
        self.name = polytope.instance.name
        self.type = polytope.instance.type
        self.graph = DiGraph()
        self.queue = []
        self.next_node = 0
        self.height = 0
        self.root = 1
        self.polytope = polytope
        self.intersections = Intersections(polytope)
        self.height = 0
        self.counter = 0
        self.threshold = -1

    def build_tree(self, threshold: int = INFINITY):
        self.threshold = threshold
        region = Region()
        solutions = list(self.polytope.vertices.keys())
        hyperplanes = list(self.polytope.H.keys())
        tree = self.get_subtree(region, solutions, hyperplanes, len(solutions) - 1, 1)
        print(tree.id)
        print(tree.get_repr())
        self.generate_tree(tree.id)
        print(self.graph)

    def get_subtree(self, region: Region, solutions: List[int], hyperplanes: List[int], max_region: int, depth: int) -> Subtree:
        self.counter = self.counter + 1
        print('\t' * (depth - 1), 'get_subtree:', self.counter, depth, region.hyperplanes, solutions)
        subtree = Subtree(self.name, self.type, region, solutions, hyperplanes)
        doc = subtree.get_doc()
        lb = ceil(log2(len(solutions)))
        ub = len(solutions) - 1

        if doc is not None and (subtree.threshold == -1 or subtree.threshold >= self.threshold):
            print('\t' * depth, f'{Fore.BLUE}', 'loading:', subtree.region, subtree.id, subtree.height, f'{Style.RESET_ALL}')
            return subtree
        else:
            if len(solutions) == 1:
                subtree.hyperplane = 0
                subtree.height = 0
                subtree.left = solutions[0]
                subtree.right = solutions[0]
                subtree.unexplored = []
                subtree.threshold = -1
                subtree.add_doc()
                print('\t' * depth, f'{Fore.LIGHTGREEN_EX}', 'writing:', subtree.region, subtree.id, subtree.height, f'{Style.RESET_ALL}')
                return subtree
            elif len(solutions) == 2:
                subtree.hyperplane = self.polytope.get_bisector(solutions[0], solutions[1])
                subtree.height = 1

                if self.polytope.get_hyperplane(subtree.hyperplane).in_halfspace(self.polytope.vertices[solutions[0]]):
                    subtree.left = solutions[1]
                    subtree.right = solutions[0]
                else:
                    subtree.left = solutions[0]
                    subtree.right = solutions[1]

                subtree.unexplored = []
                subtree.threshold = -1
                subtree.add_doc()
                print('\t' * depth, f'{Fore.LIGHTGREEN_EX}', 'writing:', subtree.region, subtree.id, subtree.height, f'{Style.RESET_ALL}')
                return subtree
            else:
                positions = self.intersections.get_positions(region, solutions)
                min_height = ub

                subtree.hyperplane = 0
                subtree.height = INFINITY
                subtree.left = 0
                subtree.right = 0
                valid_tree = False
                optimal_tree = False
                counter = 0

                for h in subtree.unexplored:
                    if min_height <= lb and valid_tree:
                        optimal_tree = True
                        break

                    # print('\t' * depth, h, counter, self.threshold)
                    if counter >= self.threshold:
                        break

                    if len(region.hyperplanes) + min_height < max_region:
                        max_region = len(region.hyperplanes) + min_height

                    if 0 < len(positions[h].left) < len(solutions) and 0 < len(positions[h].right) < len(solutions):
                        left_solutions = [item for item in solutions if item not in positions[h].right]
                        right_solutions = [item for item in solutions if item not in positions[h].left]
                        left_region = Region(region.hyperplanes)
                        right_region = Region(region.hyperplanes)
                        left_region.add_hyperplane(-h)
                        right_region.add_hyperplane(h)
                        new_hyperplanes = hyperplanes.copy()
                        new_hyperplanes.remove(h)
                        left_subtree = self.get_subtree(left_region, left_solutions, new_hyperplanes, max_region, depth + 1)

                        if left_subtree.height <= min_height:
                            right_subtree = self.get_subtree(right_region, right_solutions, new_hyperplanes, max_region, depth + 1)
                            height = max(left_subtree.height, right_subtree.height)

                            if height < min_height:
                                min_height = height + 1
                                subtree.hyperplane = h
                                subtree.height = height + 1
                                subtree.left = left_subtree.id
                                subtree.right = right_subtree.id
                                valid_tree = True

                        counter = counter + 1
                    # print('\t' * depth, 'here')

                    subtree.unexplored.remove(h)

                if optimal_tree or len(subtree.unexplored) == 0:
                    subtree.unexplored = []
                    subtree.threshold = -1
                else:
                    subtree.threshold = self.threshold

                subtree.add_doc()
                print('\t' * depth, f'{Fore.LIGHTGREEN_EX}', 'writing:', subtree.region, subtree.id, subtree.height, f'{Style.RESET_ALL}')
                return subtree

    def generate_tree(self, root_id):
        root_subtree = Subtree.from_id(root_id)
        root_node = self.__add_node(0, root_subtree)
        self.queue.append((root_node, root_subtree))

        while len(self.queue) > 0:
            parent_node, parent_subtree = self.queue.pop(0)
            node = self.graph.nodes[parent_node]
            node['hyperplane'] = parent_subtree.hyperplane
            height = node['height']

            if isinstance(parent_subtree.left, str):
                left_subtree = Subtree.from_id(parent_subtree.left)
                left_node = self.__add_node(height + 1, left_subtree)
                self.graph.add_edge(parent_node, left_node, direction='left')
                self.queue.append((left_node, left_subtree))
            else:
                left_region = deepcopy(node['region'])
                left_region.add_hyperplane(-parent_subtree.hyperplane)
                left_subtree = Subtree(self.name, self.type, left_region, [parent_subtree.left], [])
                left_node = self.__add_node(height + 1, left_subtree)
                self.graph.add_edge(parent_node, left_node, direction='left')

            if isinstance(parent_subtree.right, str):
                right_subtree = Subtree.from_id(parent_subtree.right)
                right_node = self.__add_node(height + 1, right_subtree)
                self.graph.add_edge(parent_node, right_node, direction='right')
                self.queue.append((right_node, right_subtree))
            else:
                right_region = deepcopy(node['region'])
                right_region.add_hyperplane(parent_subtree.hyperplane)
                right_subtree = Subtree(self.name, self.type, right_region, [parent_subtree.right], [])
                right_node = self.__add_node(height + 1, right_subtree)
                self.graph.add_edge(parent_node, right_node, direction='right')

    def __add_node(self, height: int, subtree: Subtree) -> int:
        """Adds a node to the tree and updates its height.

        Args:
            height: Node height.

        Returns:
            Index of the inserted node.
        """
        self.graph.add_node(self.__get_next_node(), height=height, solutions=subtree.solutions, region=Region(subtree.region))
        self.height = max(self.height, height)

        return self.next_node

    def __get_next_node(self):
        """Increments and returns the next node.
        """
        self.next_node = self.next_node + 1
        return self.next_node
