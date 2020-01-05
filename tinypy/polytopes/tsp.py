from math import factorial
from typing import List

from tinypy.geometry import Point, Hyperplane
from tinypy.polytopes import Polytope
from tinypy.utils import combinatorics


class TSP(Polytope):

    def __init__(self, size: int):
        if size <= 3 or size > 20:
            raise ValueError('The size must be greater than 3.')

        self.nodes = list(map(chr, range(65, 65 + size)))
        Polytope.__init__(self, size, int((size * (size - 1)) / 2), 'tsp')

    def get_vertices(self) -> List[Point]:
        edges = self.__get_edges()
        permutations = combinatorics.get_permutations(self.nodes)
        permutations = [''.join(p) + p[0] for p in permutations]
        vertices = []

        for permutation in permutations:
            edge = self.__get_edges_from_permutation(permutation)
            coords = [1 if e in edge else 0 for e in edges]
            vertices.append(Point(coords))

        vertices = list(set(vertices))
        vertices.sort()

        return vertices

    def get_facets(self) -> List[Hyperplane]:
        return []

    def __get_edges(self) -> List[str]:
        edges = []

        for i in range(0, self.size):
            for j in range(i + 1, self.size):
                edges.append(self.nodes[i] + self.nodes[j])

        return edges

    def __get_edges_from_permutation(self, permutation: List[str]):
        edges = []

        for i in range(self.size):
            if permutation[i] < permutation[i + 1]:
                edges.append(permutation[i] + permutation[i + 1])
            else:
                edges.append(permutation[i + 1] + permutation[i])

        return edges
