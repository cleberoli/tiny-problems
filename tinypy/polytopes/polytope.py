from abc import ABC
from abc import abstractmethod
from typing import Dict

from tinypy.geometry import Point, Hyperplane, Cone, VoronoiDiagram


class Polytope(ABC):

    def __init__(self, full_name: str, short_name: str, n: int, d: int, size: int = None):
        self.__full_name = full_name
        self.__short_name = short_name
        self.n = n
        self.d = d
        self.size = size

        self.__original_vertices = self.get_vertices()
        self.__vertices = self.__original_vertices.copy()
        print(self.__original_vertices)
        self.map_vertices()
        print(self.__vertices)

        self.__voronoi = self.get_voronoi()
        self.__cones = self.get_cones()
        self.save()

    @property
    def name(self) -> str:
        return self.__short_name

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

    def save(self):
        pad_n = len(str(self.n))
        print(pad_n)
        print(self.full_name.upper())
        print(f'DIM = {self.d}')
        print(f'N = {len(self.vertices)}')
        print()
        print('VERTICES')

        for (key, value) in self.__original_vertices.items():
            print(f'{str(key).rjust(pad_n, " ")}: {value}')

        print()
        print('SKELETON')

        for key in self.__vertices.keys():
            print(str(key).rjust(pad_n, " "), self.voronoi.delaunay.get_edges(key))

    def __repr__(self):
        return f'name: {self.name}\n' \
               f'size: {self.k}\n' \
               f'dimension: {self.d}\n'
