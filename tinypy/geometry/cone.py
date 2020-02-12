from typing import Dict

from tinypy.geometry import Hyperplane, Point, Region


class Cone(Region):

    def __init__(self, tag: int, solution: 'Point', hyperplanes: Dict[int, 'Hyperplane'], dim: int):
        Region.__init__(self, dim, hyperplanes)
        self.tag = tag
        self.solution = solution
