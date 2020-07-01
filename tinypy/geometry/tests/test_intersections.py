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
    positions = intersections.get_positions(space, [], [])

    assert positions[1].left == [1, 3, 5, 7]
    assert positions[1].right == [2, 4, 6, 8]
    assert positions[2].left == [1, 2, 5, 6]
    assert positions[2].right == [3, 4, 7, 8]
    assert positions[3].left == [1, 2, 3, 4]
    assert positions[3].right == [5, 6, 7, 8]


def test_get_positions_region():
    intersections = Intersections(cub3)
    positions = intersections.get_positions(Region(), [], [])
    positions = intersections.get_positions(Region([1]), positions[1].left, [1])

    assert positions[2].left == [2, 6]
    assert positions[2].right == [4, 8]
    assert positions[3].left == [2, 4]
    assert positions[3].right == [6, 8]

    positions = intersections.get_positions(Region(), [], [])
    positions = intersections.get_positions(Region([-1]), positions[1].right, [1])
    assert positions[2].left == [1, 5]
    assert positions[2].right == [3, 7]
    assert positions[3].left == [1, 3]
    assert positions[3].right == [5, 7]

    assert file_exists(get_full_path('files', 'lps', 'intersection', 'CUB-n3'))
    intersections.clear_lp_files()
    assert not file_exists(get_full_path('files', 'lps', 'intersection', 'CUB-n3'))

    assert file_exists(get_full_path('files', 'intersections', 'cub'))
    intersections.clear_files()
    assert not file_exists(get_full_path('files', 'intersections', 'cub'))
