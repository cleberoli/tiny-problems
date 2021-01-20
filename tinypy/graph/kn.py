from math import floor
from typing import List

from tinypy.geometry.point import Point
from tinypy.utils.combinatorics import get_combinations, get_permutations


class Kn:
    """Represents the complete graph with n nodes.

    Attributes:
        n: The number of nodes.
        nodes: List of nodes [1..n].
        edges: List of edges.
    """

    n: int
    nodes: List[int]
    edges: List[str]

    def __init__(self, n: int):
        """Initializes the Kn graph.

        Args:
            n: The number of nodes.
        """
        if n <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        self.n = n
        self.nodes = list(range(1, n + 1))
        self.edges = []

        for i in range(0, self.n):
            for j in range(i + 1, self.n):
                self.edges.append(f'{self.nodes[i]}-{self.nodes[j]}')

    def get_hamilton_cycles(self) -> List[Point]:
        """Returns all Hamiltonian cycles.

        Returns:
            All Hamiltonian cycles as points.
        """
        permutations = get_permutations(self.nodes[1:])
        permutations = [(self.nodes[0], ) + p + (self.nodes[0], ) for p in permutations]
        cycles = set()

        for permutation in permutations:
            cycles.add(self.__get_point_from_permutation(permutation))

        cycles = list(cycles)
        cycles.sort()

        return cycles

    def get_cuts(self) -> List[Point]:
        """Returns all possible cuts.

        Returns:
            All cuts as points that represent that edges to be removed.
        """
        cuts = set()

        for i in range(1, floor(self.n / 2) + 1):
            combinations = get_combinations(self.nodes, i)

            for combination in combinations:
                combination = list(combination)
                complement = [node for node in self.nodes if node not in combination]
                cuts.add(self.__get_point_from_partition(combination, complement))

        cuts = list(cuts)
        cuts.sort()

        return cuts

    def get_triangles(self) -> List[List[int]]:
        """Returns all triangles.

        Returns:
            A list containing the triangles with each triangle being represented
            by a list of three vertices.
        """
        triangles = []

        for i in range(self.n):
            for j in range(i + 1, self.n):
                for k in range(j + 1, self.n):
                    triangle = [f'{self.nodes[i]}-{self.nodes[j]}',
                                f'{self.nodes[i]}-{self.nodes[k]}',
                                f'{self.nodes[j]}-{self.nodes[k]}']
                    point = self.__get_point_from_edges(triangle)
                    indices = [i for i, e in enumerate(point.coords) if e == 1]
                    triangles.append(indices)

        return triangles

    def __get_point_from_permutation(self, permutation: tuple) -> Point:
        """Returns a point from a permutation of the nodes.

        Args:
            permutation: Permutation of the nodes.
        """
        edges = []

        for i in range(self.n):
            if permutation[i] < permutation[i + 1]:
                edges.append(f'{permutation[i]}-{permutation[i + 1]}')
            else:
                edges.append(f'{permutation[i + 1]}-{permutation[i]}')

        return self.__get_point_from_edges(edges)

    def __get_point_from_partition(self, a: List[int], b: List[int]) -> Point:
        """Returns a point from a partition of the nodes.

        Args:
            a: One set of the partition.
            b: Other set of the partition.
        """
        edges = []

        for i in range(len(a)):
            for j in range(len(b)):
                if a[i] < b[j]:
                    edges.append(f'{a[i]}-{b[j]}')
                else:
                    edges.append(f'{b[j]}-{a[i]}')

        return self.__get_point_from_edges(edges)

    def __get_point_from_edges(self, edges: List[str]) -> Point:
        """Returns a point from a list of edges.

        Args:
            edges: List of edges.
        """
        coords = [1 if e in edges else 0 for e in self.edges]
        return Point(coords)
