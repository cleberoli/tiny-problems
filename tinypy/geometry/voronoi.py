from tinypy.graph import DelaunayTriangulation
from tinypy.lp import AdjacencyProblem


class VoronoiDiagram:

    def __init__(self):
        self.delaunay = DelaunayTriangulation()

    def build(self, polytope):
        self.__get_delaunay(polytope)

    def __get_delaunay(self, polytope):
        adjacency_lp = AdjacencyProblem(polytope.dim, polytope.name, polytope.vertices)

        for i in range(polytope.n):
            for j in range(i + 1, polytope.n):
                if adjacency_lp.test_edge_primal(i, j):
                    self.delaunay.add_edge(i, j)
