from typing import List

from tinypy.geometry.point import Point
from tinypy.geometry.region import Region


class Cone(Region):

    tag: int
    solution: 'Point'

    def __init__(self, tag: int, solution: 'Point', hyperplanes: List[int] = None):
        self.tag = tag
        self.solution = solution

        Region.__init__(self, hyperplanes)
