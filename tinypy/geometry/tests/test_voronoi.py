from tinypy.geometry.voronoi import VoronoiDiagram
from tinypy.graph.delaunay import DelaunayTriangulation
from tinypy.graph.skeleton import Skeleton
from tinypy.instances.tsp_instance import TSPInstance


def test_voronoi():
    instance = TSPInstance(n=4)
    delaunay = DelaunayTriangulation(Skeleton())
    hyperplanes = dict()
    solutions = instance.get_solution_dict()
    voronoi = VoronoiDiagram(instance, delaunay, hyperplanes)

    assert voronoi.type == 'tsp'
    assert voronoi.name == 'TSP-n4'

    voronoi.build(solutions)
    voronoi.build(solutions)
