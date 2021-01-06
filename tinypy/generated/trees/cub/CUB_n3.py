from tinypy.generated.trees.generated_tree import GeneratedTree

from tinypy.geometry.point import Point


class CUBTree(GeneratedTree):

    def __init__(self, polytope):
        GeneratedTree.__init__(self, polytope)

    def test(self, point: Point):
        if self.hyperplanes[1].in_halfspace(point):
            if self.hyperplanes[2].in_halfspace(point):
                if self.hyperplanes[3].in_halfspace(point):
                    return 1, 7, 3, [1, 2, 3]
                else:
                    return 5, 6, 3, [1, 2, -3]
            else:
                if self.hyperplanes[3].in_halfspace(point):
                    return 3, 9, 3, [1, -2, 3]
                else:
                    return 7, 8, 3, [1, -2, -3]
        else:
            if self.hyperplanes[2].in_halfspace(point):
                if self.hyperplanes[3].in_halfspace(point):
                    return 2, 13, 3, [-1, 2, 3]
                else:
                    return 6, 12, 3, [-1, 2, -3]
            else:
                if self.hyperplanes[3].in_halfspace(point):
                    return 4, 15, 3, [-1, -2, 3]
                else:
                    return 8, 14, 3, [-1, -2, -3]
