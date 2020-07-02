from typing import Dict

from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.point import Point
from tinypy.polytopes.base_polytope import Polytope


class CUBTree:

    polytope: Polytope
    hyperplanes: Dict[int, Hyperplane]

    def __init__(self, polytope):
        self.polytope = polytope
        self.hyperplanes = polytope.H

    def test(self, point: Point):
        if self.hyperplanes[1].in_halfspace(point):
            if self.hyperplanes[2].in_halfspace(point):
                if self.hyperplanes[3].in_halfspace(point):
                    return 8
                else:
                    return 4
            else:
                if self.hyperplanes[3].in_halfspace(point):
                    return 6
                else:
                    return 2
        else:
            if self.hyperplanes[2].in_halfspace(point):
                if self.hyperplanes[3].in_halfspace(point):
                    return 7
                else:
                    return 3
            else:
                if self.hyperplanes[3].in_halfspace(point):
                    return 5
                else:
                    return 1
