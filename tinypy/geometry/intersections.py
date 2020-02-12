from copy import deepcopy
import pickle
from pprint import pformat

from typing import Dict
from tinypy.geometry import Hyperplane, Region, Bisection, Cone
from tinypy.lp import IntersectionProblem


class Intersections:

    def __init__(self, cones: Dict[int, 'Cone'], hyperplanes: Dict[int, 'Hyperplane'], dim: int, region: 'Region' = None, filename: str = 'default',
                 intersections: dict = None, positions: dict = None, write=True):
        self.__filename = filename
        self.__cones = cones
        self.__hyperplanes = hyperplanes
        self.__dim = dim
        self.__region = region if region is not None else Region(dim)

        if intersections is None:
            self.__intersections = dict()
            self.__positions = dict()
            self.compute_intersections()
            self.compute_positions()
        else:
            self.__intersections = intersections
            self.__positions = positions

        if write:
            self.write(f'{self.__filename}.pk')

    @classmethod
    def from_file(cls, filename: str):
        intersection = cls.read(filename)
        return cls(intersection.__cones, intersection.__hyperplanes, intersection.__dim, intersection.__region, intersection.__filename,
                   intersection.__intersections, intersection.__positions, False)

    @property
    def intersections(self):
        return self.__intersections

    @property
    def positions(self):
        return self.__positions

    def compute_intersections(self):
        for c in self.__cones.keys():
            self.__intersections[c] = dict()

            for h in self.__hyperplanes.keys():
                self.__intersections[c][h] = self.__get_cone_intersection(c, h)

    def compute_positions(self):
        for h in self.__hyperplanes.keys():
            self.__positions[h] = Bisection()
            cones = self.get_hyperplane_intersections(h)
            cones = [i for i in cones.keys() if cones[i] is False]

            for c in cones:
                if self.__hyperplanes[h].position(self.__cones[c].solution) < 0:
                    self.__positions[h].add_left(c)
                else:
                    self.__positions[h].add_right(c)

    def write(self, filename: str):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def read(filename: str):
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def get_intersection(self, cone: int, hyperplane: int):
        return self.__intersections[cone][hyperplane]

    def get_cone_intersections(self, cone: int):
        return dict((key, self.get_intersection(cone, key)) for key in self.__hyperplanes.keys())

    def get_hyperplane_intersections(self, hyperplane: int):
        return dict((key, self.get_intersection(key, hyperplane)) for key in self.__cones.keys())

    def __get_cone_intersection(self, c: int, h: int):
        region = deepcopy(self.__cones[c])
        region = region.union(self.__region)

        intersection_lp = IntersectionProblem(region, self.__hyperplanes[h], self.__dim, str(c))
        return intersection_lp.test_intersection()

    def __repr__(self):
        # representation = dict((key, self.get_hyperplane_intersections(key)) for key in range(len(self.__hyperplanes)))
        obj = {'cones': self.__cones.keys(), 'hyperplanes': self.__hyperplanes.keys(), 'region': self.__region.hyperplanes.keys(), 'positions':
            self.__positions}
        return pformat(obj)

    def __hash__(self):
        return hash((self.__cones, self.__hyperplanes, self.__region, self.__dim))

