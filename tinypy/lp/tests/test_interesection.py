from tinypy.geometry.region import Region
from tinypy.lp.intersection import IntersectionProblem
from tinypy.polytopes.hypercube_polytope import HypercubePolytope
from tinypy.utils.file import file_exists, get_full_path

cub3 = HypercubePolytope(3)
cones = cub3.voronoi.cones
hyperplanes = cub3.H
hyperplanes.update(cub3.extended_H)


def test_intersection():
    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, [], True)

    assert intersection_lp.dim == 3
    assert intersection_lp.name == 'misc'
    assert intersection_lp.cones == cones
    assert intersection_lp.hyperplanes == hyperplanes
    assert intersection_lp.lp_directory == get_full_path('files', 'lps', 'intersection', 'misc')
    assert intersection_lp.log
    assert file_exists(get_full_path('files', 'lps', 'intersection', 'misc'))


def test_intersection_euclidean():
    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, [], True)
    assert intersection_lp.test_intersection(Region(), 8, 6)
    intersection_lp.clear_files()

    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, [[0, 1, 2]], True)
    assert not intersection_lp.test_intersection(Region(), 8, 6)
    intersection_lp.clear_files()


def test_model():
    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, [], True)
    assert not intersection_lp.test_intersection(Region(), 1, 12)
    assert not intersection_lp.test_intersection(Region(), 2, 12)
    assert not intersection_lp.test_intersection(Region(), 7, 12)
    assert not intersection_lp.test_intersection(Region(), 8, 12)
    assert intersection_lp.test_intersection(Region(), 3, 12)
    assert intersection_lp.test_intersection(Region(), 4, 12)
    assert intersection_lp.test_intersection(Region(), 5, 12)
    assert intersection_lp.test_intersection(Region(), 6, 12)

    assert not intersection_lp.test_intersection(Region(), 1, 1)
    assert not intersection_lp.test_intersection(Region(), 1, 2)
    assert not intersection_lp.test_intersection(Region(), 1, 3)


def test_log():
    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, [])
    assert not intersection_lp.log
    assert not intersection_lp.test_intersection(Region(), 1, 1)
    assert not intersection_lp.test_intersection(Region(), 1, 2)
    assert not intersection_lp.test_intersection(Region(), 1, 3)


def test_clear():
    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, [], True)
    assert file_exists(get_full_path('files', 'lps', 'intersection', 'misc'))

    intersection_lp.clear_files()
    assert not file_exists(get_full_path('files', 'lps', 'intersection', 'misc'))
