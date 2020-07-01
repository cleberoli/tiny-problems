from copy import deepcopy
from typing import Dict
import os

from tinypy.geometry import Intersections, Cone, Hyperplane, Region


class Node:

    # possible_cones já representa as soluções possíveis para esse node
    def __init__(self, height: int, possible_cones: Dict[int, 'Cone'], possible_hyperplanes: Dict[int, 'Hyperplane'], dim: int, region: 'Region',
                 path: str):
        self.__height = height
        self.__cones = possible_cones.copy()
        self.__hyperplanes = possible_hyperplanes.copy()
        self.__dim = dim
        self.__region = deepcopy(region)
        self.__path = path
        self.__left_region = deepcopy(region)
        self.__right_region = deepcopy(region)
        self.__intersections = self.__get_intersections()
        self.__hyperplane = self.choose_hyperplane()
        self.__update_region()
        self.__update_hyperplanes()
        self.left = None
        self.right = None

        print(self.__path)
        # print(self.__hyperplane)
        # print(self.__region)
        # print(self.__intersections)
        # print(self.__intersections.positions)

    @property
    def height(self):
        return self.__height

    @property
    def hyperplane(self):
        return self.__hyperplane

    @property
    def hyperplanes(self):
        return self.__hyperplanes

    @property
    def region(self):
        return self.__region

    @property
    def left_cones(self):
        return dict((key, value) for (key, value) in self.__cones.items() if key not in self.__intersections.positions[self.__hyperplane].right)

    @property
    def right_cones(self):
        return dict((key, value) for (key, value) in self.__cones.items() if key not in self.__intersections.positions[self.__hyperplane].left)

    def add_left_node(self):
        self.left = Node(self.__height + 1, self.left_cones, self.__hyperplanes, self.__dim, self.__left_region, f'{self.__path}'
                                                                                                                 f'_{self.__hyperplane}L')
        return self.left

    def add_right_node(self):
        self.right = Node(self.__height + 1, self.right_cones, self.__hyperplanes, self.__dim, self.__right_region, f'{self.__path}'
                                                                                                                 f'_{self.__hyperplane}R')
        return self.right

    def choose_hyperplane(self) -> int:
        max_cuts = [self.__f(len(self.__intersections.positions[h].left), len(self.__intersections.positions[h].right), len(self.__cones))
                    for h in self.__hyperplanes.keys()]
        max_cut = max(max_cuts)

        for h in self.__hyperplanes.keys():
            if self.__f(len(self.__intersections.positions[h].left), len(self.__intersections.positions[h].right), len(self.__cones))  == max_cut:
                return h

    def __update_hyperplanes(self):
        self.__hyperplanes.pop(self.__hyperplane)

    def __update_region(self):
        self.__left_region.add_hyperplane(self.__hyperplane, -self.__hyperplanes[self.__hyperplane])
        self.__right_region.add_hyperplane(self.__hyperplane, self.__hyperplanes[self.__hyperplane])

    def __get_intersections(self):
        if os.path.exists(f'{self.__path}.pk'):
            return Intersections.from_file(f'{self.__path}.pk')
        else:
            return Intersections(self.__cones, self.__hyperplanes, self.__dim, self.__region, self.__path)

    @staticmethod
    def __f(x: int, y: int, s: int) -> float:
        return (min(((s-x) ** 2) / (s/2) ** 2, ((s-y) ** 2) / (s/2) ** 2)) * (((x-y) ** 2 + 2*x*y) / (s/2) ** 2)
