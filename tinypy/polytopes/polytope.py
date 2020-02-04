from abc import ABC
from abc import abstractmethod
from typing import List

from tinypy.geometry import Point, Hyperplane, VoronoiDiagram, Cone


class Polytope(ABC):

    def __init__(self, size: int, dim: int, name: str):
        self.size = size
        self.dim = dim
        self.name = name

        self.__vertices = self.get_vertices()
        self.__facets = self.get_facets()
        self.__voronoi = self.get_voronoi()
        self.__cones = self.get_cones()

    @property
    def vertices(self) -> List['Point']:
        return self.__vertices

    @property
    def solutions(self) -> List['Point']:
        return self.__vertices

    @property
    def facets(self) -> List['Hyperplane']:
        return self.__facets

    @property
    def voronoi(self):
        return self.__voronoi

    @property
    def cones(self):
        return self.__cones

    @abstractmethod
    def get_vertices(self) -> List['Point']:
        pass

    @abstractmethod
    def get_facets(self) -> List['Hyperplane']:
        pass

    def get_voronoi(self) -> VoronoiDiagram:
        voronoi = VoronoiDiagram()
        voronoi.build(self.dim, self.name, self.vertices)
        return voronoi

    def get_cones(self) -> dict:
        cones = dict()

        for vertex, v in zip(self.vertices, range(len(self.vertices))):
            edges = self.voronoi.get_edges(v)
            hyperplanes = [edges[e]['h'] for e in edges]
            hyperplanes.sort()

            hyperplanes = [self.voronoi.hyperplanes[h] for h in hyperplanes]
            hyperplanes = [h if h.position(vertex) >= 0 else -h for h in hyperplanes]
            cones[v] = Cone(v, vertex, hyperplanes, self.dim)

        return cones

    @staticmethod
    def __get_cone(hyperplanes: List[Hyperplane], vertex: Point):
        hyperplanes = [h if h.position(vertex) >= 0 else -h for h in hyperplanes]
        print(hyperplanes)

    def __repr__(self):
        return f'name: {self.name}\n' \
               f'size: {self.size}\n' \
               f'dimension: {self.dim}\n'
