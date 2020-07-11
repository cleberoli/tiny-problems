from typing import List

from tinypy.geometry.point import Point
from tinypy.geometry.region import Region


class Cone(Region):
    """Special case of a region.

    Each cone corresponds to a solution, and the points in this region follows
    the standard definition of a cone.

    Attributes:
        tag: Integer tag identifying the cone.
        solution: Corresponding solution.
    """

    tag: int
    solution: 'Point'

    def __init__(self, tag: int, solution: 'Point', hyperplanes: List[int] = None):
        """Initializes the cone.

        Args:
            tag: Integer tag identifying the cone.
            solution: Corresponding solution.
            hyperplanes: List of hyperplane indices.
        """
        self.tag = tag
        self.solution = solution

        Region.__init__(self, hyperplanes)
