from abc import ABC
from typing import Dict

from tinypy.geometry.point import Point
from tinypy.geometry.hyperplane import Hyperplane
# from tinypy.geometry.cone import Cone
# from tinypy.geometry.voronoi import VoronoiDiagram
from tinypy.graph.skeleton import Skeleton
from tinypy.instances.base_instance import Instance
# from tinypy.lp import AdjacencyProblem


class Polytope(ABC):

    instance: Instance
    full_name: str
    name: str
    dimension: int
    size: int
    n: int
    skeleton: Skeleton
    H: Dict[int, 'Hyperplane']

    def __init__(self):
        self.name = self.instance.type
        self.dimension = self.instance.dimension
        self.size = self.instance.size
        self.n = self.instance.n

        self.vertices = self.instance.get_solution_dict().copy()
        self.__map_vertices()

        # self.__skeleton = Skeleton()
        # self.__build_skeleton()
        #
        # self.__voronoi = self.get_voronoi()
        # self.__cones = self.get_cones()
        # self.save()

    def __map_vertices(self):
        one = Point([1] * self.dimension)

        for (key, value) in self.vertices.items():
            self.vertices[key] = (2 * value) - one

    # def get_voronoi(self) -> VoronoiDiagram:
    #     voronoi = VoronoiDiagram()
    #     voronoi.build(self.dimension, self.name, self.vertices)
    #     return voronoi
    #
    # def get_cones(self) -> Dict[int, 'Cone']:
    #     cones = dict()
    #
    #     for (v, vertex) in self.vertices.items():
    #         edges = self.voronoi.get_edges(v)
    #         hyperplanes = [edges[e]['h'] for e in edges]
    #         hyperplanes_dict = dict()
    #
    #         for h in hyperplanes:
    #             hyperplane = self.voronoi.hyperplanes[h]
    #             if hyperplane.position(vertex) >= 0:
    #                 hyperplanes_dict[h] = hyperplane
    #             else:
    #                 hyperplanes_dict[h] = -hyperplane
    #
    #         cones[v] = Cone(v, vertex, hyperplanes_dict, self.dimension)
    #
    #     return cones
    #
    # def __build_skeleton(self):
    #     adjacency_lp = AdjacencyProblem(self.dimension, self.name, self.vertices)
    #     hyperplanes = set()
    #
    #     for i in range(self.n):
    #         for j in range(i + 1, self.n):
    #             if adjacency_lp.test_edge_primal(i, j):
    #                 h = Hyperplane(self.vertices[i] - self.vertices[j], d=0)
    #                 hyperplanes.add(h)
    #                 self.__skeleton.add_edge(i, j, h=hash(h))
    #
    #     hyperplanes = list(hyperplanes)
    #     hyperplanes.sort()
    #     self.__H = dict((key, hyperplanes[key]) for key in range(len(hyperplanes)))
    #     self.__update_skeleton_hyperplanes()
    #
    # def __update_skeleton_hyperplanes(self):
    #     map_dict = {hash(self.__H[i]): i for i in range(len(self.__H))}
    #
    #     for e in self.__skeleton.edges.data():
    #         self.__skeleton.add_edge(e[0], e[1], h=map_dict[e[2]['h']])
    #
    # def save(self):
    #     pad_n = len(str(self.n))
    #     pad_m = len(str(len(self.__H)))
    #     print(pad_n)
    #     print(self.full_name.upper())
    #     print(f'DIM = {self.d}')
    #     print(f'N = {len(self.vertices)}')
    #     print()
    #     print('VERTICES')
    #
    #     for (key, value) in self.instance.get_solution_dict().items():
    #         print(f'{str(key).rjust(pad_n, " ")}: {value}')
    #
    #     print()
    #     print('HYPERPLANES')
    #
    #     for (key, value) in self.__H.items():
    #         print(f'{str(key).rjust(pad_m, " ")}: {value.normal} = {value.d}')
    #
    #     print()
    #     print('SKELETON')
    #
    #     for key in self.instance.get_solution_dict().keys():
    #         print(f'{str(key).rjust(pad_n, " ")}: {self.__skeleton.get_edges(key)}')

    def __repr__(self):  # pragma: no cover
        return f'name: {self.name}\n' \
               f'size: {self.size}\n' \
               f'dimension: {self.dimension}\n'
