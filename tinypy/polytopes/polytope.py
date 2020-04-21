from abc import ABC
from abc import abstractmethod
from typing import Dict

from tinypy.geometry import Point, Hyperplane, Cone, VoronoiDiagram
from tinypy.graph import Skeleton
from tinypy.lp import AdjacencyProblem


class Polytope(ABC):

    __full_name: str
    __short_name: str
    __n: int
    __d: int
    __size: int
    __skeleton: Skeleton
    __H: Dict[int, 'Hyperplane']

    def __init__(self, full_name: str, short_name: str, n: int, d: int, size: int = None):
        self.__full_name = full_name
        self.__short_name = short_name
        self.__n = n
        self.__d = d
        self.size = size

        self.__original_vertices = self.get_vertices()
        self.__vertices = self.__original_vertices.copy()
        self.map_vertices()

        self.__skeleton = Skeleton()
        self.__build_skeleton()
        #
        # self.__voronoi = self.get_voronoi()
        # self.__cones = self.get_cones()
        self.save()

    @property
    def name(self) -> str:
        return self.__short_name

    @property
    def d(self) -> int:
        return self.__d

    @property
    def n(self) -> int:
        return self.__n

    @property
    def vertices(self) -> Dict[int, 'Point']:
        return self.__vertices

    @property
    def voronoi(self) -> VoronoiDiagram:
        return self.__voronoi

    @property
    def cones(self) -> Dict[int, 'Cone']:
        return self.__cones

    @abstractmethod
    def get_vertices(self) -> Dict[int, 'Point']:
        pass

    def map_vertices(self):
        one = Point([1] * self.d)

        for (key, value) in self.__vertices.items():
            self.__vertices[key] = 2 * value - one

    def get_voronoi(self) -> VoronoiDiagram:
        voronoi = VoronoiDiagram()
        voronoi.build(self.d, self.name, self.vertices)
        return voronoi

    def get_cones(self) -> Dict[int, 'Cone']:
        cones = dict()

        for (v, vertex) in self.vertices.items():
            edges = self.voronoi.get_edges(v)
            hyperplanes = [edges[e]['h'] for e in edges]
            hyperplanes_dict = dict()

            for h in hyperplanes:
                hyperplane = self.voronoi.hyperplanes[h]
                if hyperplane.position(vertex) >= 0:
                    hyperplanes_dict[h] = hyperplane
                else:
                    hyperplanes_dict[h] = -hyperplane

            cones[v] = Cone(v, vertex, hyperplanes_dict, self.d)

        return cones

    def __build_skeleton(self):
        adjacency_lp = AdjacencyProblem(self.d, self.name, self.vertices)
        hyperplanes = set()

        for i in range(self.n):
            for j in range(i + 1, self.n):
                if adjacency_lp.test_edge_primal(i, j):
                    h = Hyperplane(self.vertices[i] - self.vertices[j], d=0)
                    hyperplanes.add(h)
                    self.__skeleton.add_edge(i, j, h=hash(h))

        hyperplanes = list(hyperplanes)
        hyperplanes.sort()
        self.__H = dict((key, hyperplanes[key]) for key in range(len(hyperplanes)))
        self.__update_skeleton_hyperplanes()

    def __update_skeleton_hyperplanes(self):
        map_dict = {hash(self.__H[i]): i for i in range(len(self.__H))}

        for e in self.__skeleton.edges.data():
            self.__skeleton.add_edge(e[0], e[1], h=map_dict[e[2]['h']])

    def save(self):
        pad_n = len(str(self.n))
        pad_m = len(str(len(self.__H)))
        print(pad_n)
        print(self.__full_name.upper())
        print(f'DIM = {self.d}')
        print(f'N = {len(self.vertices)}')
        print()
        print('VERTICES')

        for (key, value) in self.__original_vertices.items():
            print(f'{str(key).rjust(pad_n, " ")}: {value}')

        print()
        print('HYPERPLANES')

        for (key, value) in self.__H.items():
            print(f'{str(key).rjust(pad_m, " ")}: {value.normal} = {value.d}')

        print()
        print('SKELETON')

        for key in self.__vertices.keys():
            print(f'{str(key).rjust(pad_n, " ")}: {self.__skeleton.get_edges(key)}')

    def __repr__(self):
        return f'name: {self.name}\n' \
               f'size: {self.size}\n' \
               f'dimension: {self.d}\n'
