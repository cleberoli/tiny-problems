from abc import ABC
from abc import abstractmethod
from typing import List
from tinypy.geometry import Point, Hyperplane, VoronoiDiagram


class Polytope(ABC):

    def __init__(self, size: int, dim: int, name: str):
        self.size = size
        self.dim = dim
        self.name = name

        self.__vertices = self.get_vertices()
        self.n = len(self.__vertices)

        self.__facets = self.get_facets()
        self.__voronoi = self.get_voronoi()

    @property
    def vertices(self) -> List[Point]:
        return self.__vertices

    @property
    def solutions(self) -> List[Point]:
        return self.__vertices

    @property
    def facets(self) -> List[Hyperplane]:
        return self.__facets

    @property
    def voronoi(self):
        return self.__voronoi

    @abstractmethod
    def get_vertices(self) -> List[Point]:
        pass

    @abstractmethod
    def get_facets(self) -> List[Hyperplane]:
        pass

    def get_voronoi(self) -> VoronoiDiagram:
        voronoi = VoronoiDiagram()
        voronoi.build(self)
        return voronoi

    def __repr__(self):
        return f'name: {self.name}\n' \
               f'size: {self.size}\n' \
               f'dimension: {self.dim}\n'
