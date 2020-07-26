from tinypy.generated.trees.generated_tree import GeneratedTree

from tinypy.geometry.point import Point


class CUBTree(GeneratedTree):

    def __init__(self, polytope):
        self.polytope = polytope
        self.hyperplanes = polytope.H

    def test(self, point: Point):
        if self.hyperplanes[1].in_halfspace(point):
            if self.hyperplanes[2].in_halfspace(point):
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[4].in_halfspace(point):
                        return 1, 9, 4
                    else:
                        return 9, 8, 4
                else:
                    if self.hyperplanes[4].in_halfspace(point):
                        return 5, 11, 4
                    else:
                        return 13, 10, 4
            else:
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[4].in_halfspace(point):
                        return 3, 15, 4
                    else:
                        return 11, 14, 4
                else:
                    if self.hyperplanes[4].in_halfspace(point):
                        return 7, 17, 4
                    else:
                        return 15, 16, 4
        else:
            if self.hyperplanes[2].in_halfspace(point):
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[4].in_halfspace(point):
                        return 2, 23, 4
                    else:
                        return 10, 22, 4
                else:
                    if self.hyperplanes[4].in_halfspace(point):
                        return 6, 25, 4
                    else:
                        return 14, 24, 4
            else:
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[4].in_halfspace(point):
                        return 4, 29, 4
                    else:
                        return 12, 28, 4
                else:
                    if self.hyperplanes[4].in_halfspace(point):
                        return 8, 31, 4
                    else:
                        return 16, 30, 4
