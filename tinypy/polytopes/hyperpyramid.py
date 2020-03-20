from typing import Dict

from tinypy.geometry import Point, Hyperplane
from tinypy.polytopes import Polytope
from tinypy.utils import combinatorics


class Hyperpyramid(Polytope):

    def __init__(self, dimension: int):
        if dimension <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        Polytope.__init__(self, 'Hyperpyramid', 'pyr', 2**dimension + 1, dimension)

    def get_vertices(self) -> Dict[int, 'Point']:
        vertices = combinatorics.get_permutations([0, 2], self.d - 1)
        vertices = [Point(v + (0,)) for v in vertices]
        vertices.append(Point(tuple([1] * self.d)))

        return dict((key, vertices[key]) for key in range(len(vertices)))
