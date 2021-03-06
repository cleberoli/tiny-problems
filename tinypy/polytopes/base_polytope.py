from abc import ABC
from datetime import datetime
from typing import Dict, Tuple

from tinypy.geometry.point import Point
from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.voronoi import VoronoiDiagram
from tinypy.graph.delaunay import DelaunayTriangulation
from tinypy.graph.skeleton import Skeleton
from tinypy.instances.base_instance import Instance
from tinypy.lp.adjacency import AdjacencyProblem
from tinypy.utils.file import create_directory, file_exists, get_full_path


class Polytope(ABC):
    """Base class that build the polytopes for different instances.

    Attributes:
        full_name: The polytope full name.
        name: The instance name.
        dimension: The instance dimension.
        size: The instance size.
        n: The instance main parameter.
        skeleton_file: The path where the skeleton should be stored.
        polytope_file: The path where the polytope should be stored.
        instance: The instance.
        skeleton: The skeleton graph.
        extended_skeleton: The extended skeleton graph.
        H: The set of hyperplanes.
        extended_H: The extended set of hyperplanes.
        delaunay: The Delaunay triangulation.
        voronoi: The Voronoi diagram.
        vertices: The polytope vertices.
    """

    full_name: str
    name: str
    dimension: int
    size: int
    n: int
    skeleton_file: str
    polytope_file: str

    instance: Instance
    skeleton: Skeleton
    extended_skeleton: Skeleton
    H: Dict[int, 'Hyperplane']
    extended_H: Dict[int, 'Hyperplane']
    delaunay: DelaunayTriangulation
    voronoi: VoronoiDiagram
    vertices: Dict[int, Point]

    def __init__(self, instance: Instance, full_name: str):
        """Initializes the polytope with the given instance and name.

        Args:
            instance: The instance.
            full_name: The polytope full name.
        """
        self.instance = instance
        self.full_name = full_name
        self.name = self.instance.type
        self.dimension = self.instance.dimension
        self.size = self.instance.size
        self.n = self.instance.n
        self.skeleton_file = get_full_path('files', 'skeletons', self.instance.type, f'{self.instance.name}.tpsf')
        self.polytope_file = get_full_path('files', 'polytopes', self.instance.type, f'{self.instance.name}.tppf')
        create_directory(get_full_path('files', 'skeletons', self.instance.type))
        create_directory(get_full_path('files', 'polytopes', self.instance.type))

        self.vertices = self.instance.get_solution_dict().copy()
        self.vertices = dict((key, Point([1] * self.dimension) - 2 * point) for (key, point) in self.vertices.items())

        self.build_skeleton()
        self.delaunay = DelaunayTriangulation(self.skeleton)
        self.voronoi = VoronoiDiagram(self.delaunay, self.H, self.instance.type, self.instance.name)
        self.voronoi.build(self.vertices)

        if not file_exists(self.polytope_file):
            self.__write_polytope_file()

    def build_skeleton(self):
        """Build the polytope skeleton.

        If the skeleton has been previously computed it is loaded from the file.
        Otherwise it is generated and saved.
        """
        if file_exists(self.skeleton_file):
            self.skeleton, self.H, self.extended_skeleton, self.extended_H = self.__read_skeleton_file()
        else:
            self.skeleton, self.H, self.extended_skeleton, self.extended_H = self.__generate_skeleton()
            self.__write_skeleton_file()

    def get_bisector(self, i: int, j: int) -> int:
        """Returns the bisector of two points.

        Args:
            i: First node.
            j: Second node.

        Returns:
            The index of the bisector hyperplane, chosen from the skeleton or
            the extended skeleton.
        """
        if self.skeleton.has_edge(i, j):
            return self.skeleton.get_edge(i, j, 'h')
        else:
            return self.extended_skeleton.get_edge(i, j, 'h')

    def get_hyperplane(self, h: int) -> 'Hyperplane':
        if h in self.H.keys():
            return self.H[h]
        else:
            return self.extended_H[h]

    def __generate_skeleton(self) -> Tuple['Skeleton', Dict[int, 'Hyperplane'], 'Skeleton', Dict[int, 'Hyperplane']]:
        """Generates the skeleton along with the hyperplanes.

        Returns:
            The skeleton graph.
            The set of hyperplanes.
            The extended skeleton graph.
            The extended set of hyperplanes.
        """
        skeleton = Skeleton()
        extended_skeleton = Skeleton()
        adjacency_lp = AdjacencyProblem(self.dimension, self.instance.name, self.vertices)
        hyperplanes = set()
        extended_hyperplanes = set()
        vertices = self.instance.get_solution_dict()

        for i in range(1, self.size + 1):
            for j in range(i + 1, self.size + 1):
                h = Hyperplane(vertices[j] - vertices[i], d=0)

                if adjacency_lp.test_edge_primal(i, j):
                    hyperplanes.add(h)
                    skeleton.add_edge(i, j, h=hash(h))
                else:
                    extended_hyperplanes.add(h)
                    extended_skeleton.add_edge(i, j, h=hash(h))

        adjacency_lp.clear_files()

        hyperplanes = list(hyperplanes)
        hyperplanes.sort()
        hyperplanes = dict((key + 1, hyperplanes[key]) for key in range(len(hyperplanes)))

        extended_hyperplanes = list(extended_hyperplanes)
        extended_hyperplanes.sort()
        extended_hyperplanes = dict((key + len(hyperplanes) + 1, extended_hyperplanes[key]) for key in range(len(extended_hyperplanes)))

        map_dict = {hash(hyperplanes[i]): i for i in hyperplanes.keys()}
        extended_map_dict = {hash(extended_hyperplanes[i]): i for i in extended_hyperplanes.keys()}

        for edge in skeleton.edges:
            skeleton.add_edge(edge[0], edge[1], h=map_dict[skeleton.get_edge(edge[0], edge[1], 'h')])

        for edge in extended_skeleton.edges:
            extended_skeleton.add_edge(edge[0], edge[1], h=extended_map_dict[extended_skeleton.get_edge(edge[0], edge[1], 'h')])

        return skeleton, hyperplanes, extended_skeleton, extended_hyperplanes

    def __read_skeleton_file(self) -> Tuple['Skeleton', Dict[int, 'Hyperplane'], 'Skeleton', Dict[int, 'Hyperplane']]:
        """Loads the skeleton from the file.

        Returns:
            The skeleton graph.
            The set of hyperplanes.
            The extended skeleton graph.
            The extended set of hyperplanes.
        """
        skeleton = Skeleton()
        hyperplanes = dict()
        extended_skeleton = Skeleton()
        extended_hyperplanes = dict()

        with open(self.skeleton_file, 'r') as file:
            file.readline()     # name
            file.readline()     # type
            file.readline()     # generated
            file.readline()     # dimension
            file.readline()     # size
            h_size = int(file.readline().split()[1])
            e_size = int(file.readline().split()[1])
            e_h_size = int(file.readline().split()[2])
            e_e_size = int(file.readline().split()[2])
            file.readline()

            file.readline()     # HYPERPLANES SECTION
            for _ in range(h_size):
                line = file.readline().split(':')
                key = int(line[0].strip())
                hyperplane = list(map(int, line[1].split()))
                hyperplane = Hyperplane(Point(hyperplane[:-1]), d=hyperplane[-1])
                hyperplanes[key] = hyperplane
            file.readline()

            file.readline()     # SKELETON SECTION
            for _ in range(e_size):
                edge = list(map(int, file.readline().split()))
                skeleton.add_edge(edge[0], edge[1], h=edge[2])
            file.readline()

            file.readline()  # EXTENDED HYPERPLANES SECTION
            for _ in range(e_h_size):
                line = file.readline().split(':')
                key = int(line[0].strip())
                hyperplane = list(map(int, line[1].split()))
                hyperplane = Hyperplane(Point(hyperplane[:-1]), d=hyperplane[-1])
                extended_hyperplanes[key] = hyperplane
            file.readline()

            file.readline()  # SKELETON SECTION
            for _ in range(e_e_size):
                edge = list(map(int, file.readline().split()))
                extended_skeleton.add_edge(edge[0], edge[1], h=edge[2])

        return skeleton, hyperplanes, extended_skeleton, extended_hyperplanes

    def __write_skeleton_file(self):
        """Writes the skeleton to a file.
        """
        now = datetime.now()

        with open(self.skeleton_file, 'w+') as file:
            file.write(f'NAME: {self.instance.name}\n')
            file.write(f'TYPE: {self.instance.type.upper()}\n')
            file.write(f'GENERATED: {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
            file.write(f'DIMENSION: {self.dimension}\n')
            file.write(f'SOLUTIONS: {self.size}\n')
            file.write(f'HYPERPLANES: {len(self.H)}\n')
            file.write(f'EDGES: {len(self.skeleton.edges)}\n')
            file.write(f'EXTENDED HYPERPLANES: {len(self.extended_H)}\n')
            file.write(f'EXTENDED EDGES: {len(self.extended_skeleton.edges)}\n\n')

            file.write(f'HYPERPLANES SECTION\n')
            for (index, hyperplane) in self.H.items():
                file.write(f'{index}: {" ".join(map(str, hyperplane.normal))} {hyperplane.d}\n')
            file.write('\n')

            file.write(f'SKELETON SECTION\n')
            for edge in self.skeleton.edges:
                file.write(f'{edge[0]} {edge[1]} {self.skeleton.get_edge(edge[0], edge[1], "h")}\n')
            file.write('\n')

            file.write(f'EXTENDED HYPERPLANES SECTION\n')
            for (index, hyperplane) in self.extended_H.items():
                file.write(f'{index}: {" ".join(map(str, hyperplane.normal))} {hyperplane.d}\n')
            file.write('\n')

            file.write(f'EXTENDED SKELETON SECTION\n')
            for edge in self.extended_skeleton.edges:
                file.write(f'{edge[0]} {edge[1]} {self.extended_skeleton.get_edge(edge[0], edge[1], "h")}\n')

    def __write_polytope_file(self):
        """Writes the polytope to a file.
        """
        with open(self.polytope_file, 'w+') as file:
            file.write(repr(self))

    def __repr__(self):  # pragma: no cover
        degrees = [self.skeleton.graph.degree(i) for i in self.skeleton.graph.nodes]

        return f'NAME: {self.instance.name}\n' \
               f'TYPE: {self.instance.type.upper()}\n' \
               f'DIMENSION: {self.dimension}\n' \
               f'SOLUTIONS: {self.size}\n' \
               f'HYPERPLANES: {len(self.H)}\n' \
               f'EDGES: {len(self.skeleton.edges)}\n' \
               f'AVERAGE DEGREE: {sum(degrees) / max(len(degrees), 1)}\n'
