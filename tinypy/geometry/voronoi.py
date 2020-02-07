from typing import Dict, List

from tinypy.geometry import Hyperplane, Point
from tinypy.graph import DelaunayTriangulation
from tinypy.lp import AdjacencyProblem


class VoronoiDiagram:

    def __init__(self):
        self.delaunay = DelaunayTriangulation()
        self.__hyperplanes = dict()

    @property
    def hyperplanes(self) -> Dict[int, 'Hyperplane']:
        return self.__hyperplanes

    def get_edge(self, i: int, j: int, key: str = 'h'):
        return self.delaunay.get_edge(i, j, key)

    def get_edges(self, i: int):
        return self.delaunay.get_edges(i)

    def build(self, dim: int, name: str, vertices: Dict[int, 'Point']):
        self.__initialize(dim, name, vertices)
        self.__update()

    def __initialize(self, dim: int, name: str, vertices: Dict[int, 'Point']):
        adjacency_lp = AdjacencyProblem(dim, name, vertices)
        hyperplanes = set()
        n = len(vertices)

        for i in range(n):
            for j in range(i + 1, n):
                if adjacency_lp.test_edge_primal(i, j):
                    h = Hyperplane(vertices[i] - vertices[j], d=0)
                    hyperplanes.add(h)
                    self.delaunay.add_edge(i, j, h=hash(h))

        hyperplanes = list(hyperplanes)
        hyperplanes.sort()
        self.__hyperplanes = dict((key, hyperplanes[key]) for key in range(len(hyperplanes)))

    def __update(self):
        map_dict = {hash(self.__hyperplanes[i]): i for i in range(len(self.__hyperplanes))}

        for e in self.delaunay.edges.data():
            self.delaunay.add_edge(e[0], e[1], h=map_dict[e[2]['h']])
