from tinypy.geometry.intersections import Intersections
from tinypy.geometry.region import Region
from tinypy.polytopes.hypercube_polytope import HypercubePolytope
from tinypy.utils.file import file_exists, get_full_path

cub3 = HypercubePolytope(3)


def test_intersections():
    intersections = Intersections(cub3)

    assert intersections.hyperplanes == cub3.H
    assert intersections.cones == cub3.voronoi.cones
    assert file_exists(get_full_path('files', 'lps', 'intersection', 'CUB-n3'))


def test_get_positions():
    intersections = Intersections(cub3)
    space = Region()
    positions = intersections.get_positions(space, [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3])

    assert positions[1].left == [2, 4, 6, 8]
    assert positions[1].right == [1, 3, 5, 7]
    assert positions[2].left == [3, 4, 7, 8]
    assert positions[2].right == [1, 2, 5, 6]
    assert positions[3].left == [5, 6, 7, 8]
    assert positions[3].right == [1, 2, 3, 4]


def test_get_positions_region():
    intersections = Intersections(cub3)
    positions = intersections.get_positions(Region(), [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3])
    positions = intersections.get_positions(Region([1]), [2, 4, 6, 8], [2, 3])

    assert positions[2].left == [4, 8]
    assert positions[2].right == [2, 6]
    assert positions[3].left == [6, 8]
    assert positions[3].right == [2, 4]

    positions = intersections.get_positions(Region(), [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3])
    positions = intersections.get_positions(Region([-1]), [1, 3, 5, 7], [2, 3])
    assert positions[2].left == [3, 7]
    assert positions[2].right == [1, 5]
    assert positions[3].left == [5, 7]
    assert positions[3].right == [1, 3]

    assert file_exists(get_full_path('files', 'lps', 'intersection', 'CUB-n3'))
    intersections.clear_lp_files()
    assert not file_exists(get_full_path('files', 'lps', 'intersection', 'CUB-n3'))

    assert file_exists(get_full_path('files', 'intersections', 'cub'))
    intersections.clear_files()
    assert not file_exists(get_full_path('files', 'intersections', 'cub'))
