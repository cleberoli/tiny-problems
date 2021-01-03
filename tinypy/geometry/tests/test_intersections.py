from tinypy.geometry.intersections import Intersections
from tinypy.geometry.region import Region
from tinypy.polytopes.hypercube_polytope import HypercubePolytope
from tinypy.polytopes.tsp_polytope import TSPPolytope

cub3 = HypercubePolytope(3)
tsp5 = TSPPolytope(5)


def test_intersections():
    intersections = Intersections(cub3)

    assert intersections.hyperplanes == cub3.hyperplanes
    assert intersections.cones == cub3.voronoi.cones


def test_get_positions():
    intersections = Intersections(cub3)
    positions = intersections.get_positions(Region(), [1, 2, 3, 4, 5, 6, 7, 8])

    assert positions[1].left == [2, 4, 6, 8]
    assert positions[1].right == [1, 3, 5, 7]
    assert positions[2].left == [3, 4, 7, 8]
    assert positions[2].right == [1, 2, 5, 6]
    assert positions[3].left == [5, 6, 7, 8]
    assert positions[3].right == [1, 2, 3, 4]


def test_get_positions_region():
    intersections = Intersections(cub3)
    positions = intersections.get_positions(Region([1]), [1, 3, 5, 7])

    assert positions[2].left == [3, 7]
    assert positions[2].right == [1, 5]
    assert positions[3].left == [5, 7]
    assert positions[3].right == [1, 3]

    positions = intersections.get_positions(Region([-1]), [2, 4, 6, 8])
    assert positions[2].left == [4, 8]
    assert positions[2].right == [2, 6]
    assert positions[3].left == [6, 8]
    assert positions[3].right == [2, 4]


def test_get_positions_tsp():
    intersections = Intersections(tsp5)
    positions = intersections.get_positions(Region(), list(range(1, 13)))

    assert positions[1].left == [2, 12]
    assert positions[1].right == [1, 11]
    assert positions[2].left == [6, 8]
    assert positions[2].right == [5, 7]
    assert positions[3].left == [4, 10]
    assert positions[3].right == [3, 9]
