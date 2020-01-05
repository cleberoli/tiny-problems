from typing import List

from tinypy.geometry import Point, Hyperplane
from tinypy.polytopes import Polytope
from tinypy.utils import combinatorics


class Hyperpyramid(Polytope):

    def __init__(self, dimension: int):
        if dimension <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        Polytope.__init__(self, dimension, dimension, 'pyr')

    def get_vertices(self) -> List[Point]:
        vertices = combinatorics.get_permutations([0, 2], self.dim - 1)
        vertices = [Point(v + (0,)) for v in vertices]
        vertices.append(Point(tuple([1] * self.dim)))
        return vertices

    def get_facets(self) -> List[Hyperplane]:
        return []
