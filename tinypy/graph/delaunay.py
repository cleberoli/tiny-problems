import networkx as nx

from tinypy.geometry import Hyperplane


class DelaunayTriangulation:

    def __init__(self):
        self.__graph = nx.Graph()

    @property
    def edges(self):
        return self.__graph.edges

    def add_edge(self, i: int, j: int, h: Hyperplane = None):
        if h is None:
            self.__graph.add_edge(i, j)
        else:
            self.__graph.add_edge(i, j, hyperplane=h)
