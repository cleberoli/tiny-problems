from typing import List

from tinypy.geometry import Point, Hyperplane
from tinypy.polytopes import Polytope
from tinypy.utils import combinatorics


class Hypercube(Polytope):

    def __init__(self, dimension: int):
        if dimension <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        Polytope.__init__(self, dimension, dimension, 'cub')

    def get_vertices(self) -> List['Point']:
        vertices = combinatorics.get_permutations([0, 1], self.dim)
        vertices = [Point(v) for v in vertices]
        return vertices

    def get_facets(self) -> List['Hyperplane']:
        return []
