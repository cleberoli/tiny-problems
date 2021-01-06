from tinypy.geometry.region import Region
from tinypy.lp.intersection import IntersectionProblem
from tinypy.polytopes.hypercube_polytope import HypercubePolytope

cub3 = HypercubePolytope(3)
cones = cub3.voronoi.cones
hyperplanes = cub3.hyperplanes


def test_intersection():
    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, [])

    assert intersection_lp.dim == 3
    assert intersection_lp.name == 'misc'
    assert intersection_lp.cones == cones
    assert intersection_lp.hyperplanes == hyperplanes


def test_intersection_euclidean():
    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, [])
    left, right = intersection_lp.test_intersection(Region(), 8, 6)
    assert left and right

    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, [[0, 1, 2]])
    left, right = intersection_lp.test_intersection(Region(), 8, 6)
    assert not (left and right)


def test_model():
    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, [])
    left, right = intersection_lp.test_intersection(Region(), 1, 12)
    assert not (left and right)
    left, right = intersection_lp.test_intersection(Region(), 2, 12)
    assert not (left and right)
    left, right = intersection_lp.test_intersection(Region(), 7, 12)
    assert not (left and right)
    left, right = intersection_lp.test_intersection(Region(), 8, 12)
    assert not (left and right)

    left, right = intersection_lp.test_intersection(Region(), 3, 12)
    assert left and right
    left, right = intersection_lp.test_intersection(Region(), 4, 12)
    assert left and right
    left, right = intersection_lp.test_intersection(Region(), 5, 12)
    assert left and right
    left, right = intersection_lp.test_intersection(Region(), 6, 12)
    assert left and right
