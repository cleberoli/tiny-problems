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
                    if self.hyperplanes[4].in_halfspace(point):
                        return 16
                    else:
                        return 8
                else:
                    if self.hyperplanes[4].in_halfspace(point):
                        return 12
                    else:
                        return 4
            else:
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[4].in_halfspace(point):
                        return 14
                    else:
                        return 6
                else:
                    if self.hyperplanes[4].in_halfspace(point):
                        return 10
                    else:
                        return 2
        else:
            if self.hyperplanes[2].in_halfspace(point):
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[4].in_halfspace(point):
                        return 15
                    else:
                        return 7
                else:
                    if self.hyperplanes[4].in_halfspace(point):
                        return 11
                    else:
                        return 3
            else:
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[4].in_halfspace(point):
                        return 13
                    else:
                        return 5
                else:
                    if self.hyperplanes[4].in_halfspace(point):
                        return 9
                    else:
                        return 1
