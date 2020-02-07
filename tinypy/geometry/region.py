from bisect import insort
from typing import List

from tinypy.geometry import Hyperplane


class Region:

    def __init__(self, dim: int, hyperplanes: List['Hyperplane'] = None):
        self.__hyperplanes = hyperplanes if hyperplanes is not None else []
        self.__hyperplanes.sort()
        self.__dim = dim

    @property
    def hyperplanes(self):
        return self.__hyperplanes

    @property
    def dim(self):
        return self.__dim

    def add_hyperplane(self, hyperplane: 'Hyperplane'):
        insort(self.__hyperplanes, hyperplane)

    def union(self, region: 'Region'):
        return Region(self.__dim, self.merge_list(self.__hyperplanes, region.hyperplanes))

    @staticmethod
    def merge_list(a: List, b: list):
        for item in b:
            insort(a, item)

        return a
