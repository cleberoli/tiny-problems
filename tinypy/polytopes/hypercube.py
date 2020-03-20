from typing import Dict

from tinypy.geometry import Point, Hyperplane
from tinypy.polytopes import Polytope
from tinypy.utils import combinatorics


class Hypercube(Polytope):

    def __init__(self, dimension: int):
        if dimension <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        Polytope.__init__(self, 'Hypercube', 'cub', 2**dimension, dimension)

    def get_vertices(self) -> Dict[int, 'Point']:
        vertices = combinatorics.get_permutations([0, 1], self.d)
        vertices = [Point(v) for v in vertices]

        return dict((key, vertices[key]) for key in range(len(vertices)))
