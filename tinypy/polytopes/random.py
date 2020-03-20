from typing import Dict

from tinypy.geometry import Point, Hyperplane
from tinypy.polytopes import Polytope


class Random(Polytope):

    def __init__(self, size: int, dimension: int):
        self.x = size
        Polytope.__init__(self, dimension, dimension, 'rand')

    def get_vertices(self) -> Dict[int, 'Point']:
        vertices = [Point.random(self.dim) for _ in range(self.x)]
        vertices.sort()

        return dict((key, vertices[key]) for key in range(len(vertices)))

    def get_facets(self) -> Dict[int, 'Hyperplane']:
        return dict()
