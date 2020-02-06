from abc import ABC
from abc import abstractmethod
from typing import Dict, List

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
    def vertices(self) -> Dict[int, 'Point']:
        return self.__vertices

    @property
    def solutions(self) -> Dict[int, 'Point']:
        return self.__vertices

    @property
    def facets(self) -> Dict[int, 'Hyperplane']:
        return self.__facets

    @property
    def voronoi(self) -> VoronoiDiagram:
        return self.__voronoi

    @property
    def cones(self) -> Dict[int, 'Cone']:
        return self.__cones

    @abstractmethod
    def get_vertices(self) -> Dict[int, 'Point']:
        pass

    @abstractmethod
    def get_facets(self) -> Dict[int, 'Hyperplane']:
        pass

    def get_voronoi(self) -> VoronoiDiagram:
        voronoi = VoronoiDiagram()
        voronoi.build(self.dim, self.name, self.vertices)
        return voronoi

    def get_cones(self) -> Dict[int, 'Cone']:
        cones = dict()

        for (v, vertex) in self.vertices.items():
            edges = self.voronoi.get_edges(v)
            hyperplanes = [edges[e]['h'] for e in edges]
            hyperplanes.sort()

            hyperplanes = [self.voronoi.hyperplanes[h] for h in hyperplanes]
            hyperplanes = [h if h.position(vertex) >= 0 else -h for h in hyperplanes]
            cones[v] = Cone(v, vertex, hyperplanes, self.dim)

        return cones

    def __repr__(self):
        return f'name: {self.name}\n' \
               f'size: {self.size}\n' \
               f'dimension: {self.dim}\n'
