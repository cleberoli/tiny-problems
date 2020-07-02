from tinypy.geometry.point import Point
from tinypy.geometry.voronoi import VoronoiDiagram
from tinypy.graph.delaunay import DelaunayTriangulation
from tinypy.graph.skeleton import Skeleton
from tinypy.utils.file import delete_directory, file_exists, get_full_path


def test_voronoi():
    delaunay = DelaunayTriangulation(Skeleton())
    hyperplanes = dict()
    solutions = {1: Point(1, 1, 1)}
    voronoi = VoronoiDiagram(delaunay, hyperplanes, 'type', 'name')

    assert voronoi.instance_type == 'type'
    assert voronoi.instance_name == 'name'
    assert file_exists(get_full_path('files', 'cones', 'type'))
    assert not file_exists(get_full_path('files', 'cones', 'type', 'name.tpcf'))

    voronoi.build(solutions)
    voronoi.build(solutions)
    assert file_exists(get_full_path('files', 'cones', 'type', 'name.tpcf'))

    delete_directory(get_full_path(get_full_path('files', 'cones', 'type')))
    assert not file_exists(get_full_path('files', 'cones', 'type'))
