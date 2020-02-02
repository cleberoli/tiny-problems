from typing import List
from tinypy.geometry import Hyperplane
from tinypy.lp import IntersectionProblem


class Intersection:

    def __init__(self, cones: dict, hyperplanes: List[Hyperplane], dim: int):
        self.cones = cones
        self.hyperplanes = hyperplanes
        self.dim = dim

    def get_cone_intersection(self, h: int):
        for key, value in self.cones.items():
            intersection_lp = IntersectionProblem(value.hyperplanes, self.hyperplanes[h], self.dim, key)
            print(intersection_lp.test_intersection())
