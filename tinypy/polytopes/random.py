from typing import Dict

from tinypy.geometry import Point, Hyperplane
from tinypy.polytopes import Polytope


class Random(Polytope):

    def __init__(self, n: int, dimension: int):
        Polytope.__init__(self, 'Random', 'rand', n, dimension)

    def get_vertices(self) -> Dict[int, 'Point']:
        vertices = [Point.random(self.d) for _ in range(self.n)]
        vertices.sort()

        return dict((key, vertices[key]) for key in range(len(vertices)))
