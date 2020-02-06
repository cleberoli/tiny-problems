import pickle
from pprint import pformat

from typing import Dict
from tinypy.geometry import Hyperplane, Region, Partition
from tinypy.lp import IntersectionProblem


class Intersections:

    def __init__(self, cones: Dict[int, 'Cone'], hyperplanes: Dict[int, 'Hyperplane'], dim: int, region: 'Region' = None, intersections: dict = None,
                 write=True):
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

        if write:
            self.write('test')

    @classmethod
    def from_file(cls, filename: str):
        intersection = cls.read(filename)
        return cls(intersection.__cones, intersection.__hyperplanes, intersection.__dim, intersection.__region, intersection.__intersections, False)

    @property
    def intersections(self):
        return self.__intersections

    @property
    def positions(self):
        return self.__positions

    def compute_intersections(self):
        for c in self.__cones.keys():
            self.__intersections[c] = dict()

            for h in range(len(self.__hyperplanes)):
                self.__intersections[c][h] = self.__get_cone_intersection(c, h)

    def compute_positions(self):
        for h in range(len(self.__hyperplanes)):
            self.__positions[h] = Partition()
            cones = self.get_hyperplane_intersections(h)
            cones = [i for i in range(len(cones)) if cones[i] is False]

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
        intersection_lp = IntersectionProblem(self.__cones[c].union(self.__region), self.__hyperplanes[h], self.__dim, str(c))
        return intersection_lp.test_intersection()

    def __repr__(self):
        representation = dict((key, self.get_hyperplane_intersections(key)) for key in range(len(self.__hyperplanes)))
        return pformat(representation)
