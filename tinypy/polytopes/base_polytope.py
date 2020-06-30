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
from tinypy.utils.file import create_folder, file_exists, get_full_path


class Polytope(ABC):

    full_name: str
    name: str
    dimension: int
    size: int
    n: int
    skeleton_file: str

    instance: Instance
    skeleton: Skeleton
    H: Dict[int, 'Hyperplane']
    delaunay: DelaunayTriangulation
    voronoi: VoronoiDiagram

    def __init__(self):
        self.name = self.instance.type
        self.dimension = self.instance.dimension
        self.size = self.instance.size
        self.n = self.instance.n
        self.skeleton_file = get_full_path('files', 'skeletons', self.instance.type, f'{self.instance.name}.tpsf')
        create_folder(get_full_path('files', 'skeletons', self.instance.type))

        self.vertices = self.instance.get_solution_dict().copy()
        self.__map_vertices()

        self.build_skeleton()
        self.delaunay = DelaunayTriangulation(self.skeleton)
        self.voronoi = VoronoiDiagram(self.delaunay, self.H, self.instance.type, self.instance.name)
        self.voronoi.build(self.vertices)

    def __map_vertices(self):
        one = Point([1] * self.dimension)

        for (key, value) in self.vertices.items():
            self.vertices[key] = (2 * value) - one

    def build_skeleton(self):
        if file_exists(self.skeleton_file):
            self.skeleton, self.H = self.__read_skeleton_file()
        else:
            self.skeleton, self.H = self.__generate_skeleton()
            self.__write_skeleton_file()

    def __generate_skeleton(self) -> Tuple['Skeleton', Dict[int, 'Hyperplane']]:
        skeleton = Skeleton()
        adjacency_lp = AdjacencyProblem(self.dimension, self.instance.name, self.vertices)
        hyperplanes = set()
        vertices = self.instance.get_solution_dict()

        for i in range(1, self.size + 1):
            for j in range(i + 1, self.size + 1):
                if adjacency_lp.test_edge_primal(i, j):
                    h = Hyperplane(vertices[j] - vertices[i], d=0)
                    hyperplanes.add(h)
                    skeleton.add_edge(i, j, h=hash(h))

        adjacency_lp.clear_files()

        hyperplanes = list(hyperplanes)
        hyperplanes.sort()
        hyperplanes = dict((key + 1, hyperplanes[key]) for key in range(len(hyperplanes)))

        map_dict = {hash(hyperplanes[i]): i for i in hyperplanes.keys()}

        for edge in skeleton.edges:
            skeleton.add_edge(edge[0], edge[1], h=map_dict[skeleton.get_edge(edge[0], edge[1], 'h')])

        return skeleton, hyperplanes

    def __read_skeleton_file(self) -> Tuple['Skeleton', Dict[int, 'Hyperplane']]:
        skeleton = Skeleton()
        hyperplanes = dict()

        with open(self.skeleton_file, 'r') as file:
            file.readline()     # name
            file.readline()     # type
            file.readline()     # generated
            file.readline()     # dimension
            file.readline()     # size
            h_size = int(file.readline().split()[1])
            e_size = int(file.readline().split()[1])
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

        return skeleton, hyperplanes

    def __write_skeleton_file(self):
        now = datetime.now()

        with open(self.skeleton_file, 'w+') as file:
            file.write(f'NAME: {self.instance.name}\n')
            file.write(f'TYPE: {self.instance.type.upper()}\n')
            file.write(f'GENERATED: {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
            file.write(f'DIMENSION: {self.dimension}\n')
            file.write(f'SOLUTIONS: {self.size}\n')
            file.write(f'HYPERPLANES: {len(self.H)}\n')
            file.write(f'EDGES: {len(self.skeleton.edges)}\n\n')

            file.write(f'HYPERPLANES SECTION\n')
            for (index, hyperplane) in self.H.items():
                file.write(f'{index}: {" ".join(map(str, hyperplane.normal))} {hyperplane.d}\n')
            file.write('\n')

            file.write(f'SKELETON SECTION\n')
            for edge in self.skeleton.edges:
                file.write(f'{edge[0]} {edge[1]} {self.skeleton.get_edge(edge[0], edge[1], "h")}\n')

    def __repr__(self):  # pragma: no cover
        return f'NAME: {self.instance.type}\n' \
               f'TYPE: {self.instance.type}\n' \
               f'DIMENSION: {self.dimension}\n' \
               f'SOLUTIONS: {self.size}\n' \
               f'HYPERPLANES: {len(self.H)}\n' \
               f'EDGES: {len(self.skeleton.edges)}\n'
