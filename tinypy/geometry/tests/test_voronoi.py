from tinypy.geometry.voronoi import VoronoiDiagram
from tinypy.graph.skeleton import Skeleton
from tinypy.instances.tsp_instance import TSPInstance


def test_voronoi():
    instance = TSPInstance(n=4)
    skeleton = Skeleton()
    hyperplanes = dict()
    solutions = instance.get_solution_dict()
    voronoi = VoronoiDiagram(instance, skeleton, hyperplanes)

    assert voronoi.type == 'tsp'
    assert voronoi.name == 'TSP-n4'

    voronoi.build(solutions)
    voronoi.build(solutions)
