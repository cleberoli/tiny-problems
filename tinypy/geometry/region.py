from copy import deepcopy
from typing import Dict

from tinypy.geometry import Hyperplane


class Region:

    def __init__(self, dim: int, hyperplanes: Dict[int, 'Hyperplane'] = None):
        self.__hyperplanes = hyperplanes if hyperplanes is not None else dict()
        self.__dim = dim

    @property
    def hyperplanes(self):
        return self.__hyperplanes

    @property
    def dim(self):
        return self.__dim

    def add_hyperplane(self, key: int, hyperplane: 'Hyperplane'):
        self.__hyperplanes[key] = hyperplane

    def union(self, region: 'Region'):
        current_dict = self.__hyperplanes.copy()
        region_dict = region.hyperplanes.copy()
        return Region(self.__dim, {**current_dict, **region_dict})

    def __repr__(self):
        return str(self.__hyperplanes)
