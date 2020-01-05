from abc import ABC
from abc import abstractmethod
from typing import List
from tinypy.geometry import Point, Hyperplane


class Polytope(ABC):

    def __init__(self, size: int, dim: int, name: str):
        self.size = size
        self.name = name
        self.dim = dim

        self.__vertices = self.get_vertices()
        self.__facets = self.get_facets()

    @property
    def vertices(self) -> List[Point]:
        return self.__vertices

    @property
    def solutions(self) -> List[Point]:
        return self.__vertices

    @property
    def facets(self) -> List[Hyperplane]:
        return self.__facets

    @abstractmethod
    def get_vertices(self) -> List[Point]:
        pass

    @abstractmethod
    def get_facets(self) -> List[Hyperplane]:
        pass

    def __repr__(self):
        return f'name: {self.name}\n' \
               f'size: {self.size}\n' \
               f'dimension: {self.dim}\n'
