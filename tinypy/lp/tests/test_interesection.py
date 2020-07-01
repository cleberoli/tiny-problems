from tinypy.geometry.cone import Cone
from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.point import Point
from tinypy.geometry.region import Region
from tinypy.lp.intersection import IntersectionProblem
from tinypy.utils.file import file_exists, get_full_path

solutions = {1: Point(0, 0, 0), 2: Point(0, 0, 1),
             3: Point(0, 1, 0), 4: Point(0, 1, 1),
             5: Point(1, 0, 0), 6: Point(1, 0, 1),
             7: Point(1, 1, 0), 8: Point(1, 1, 1)}

hyperplanes = {1: Hyperplane(Point(0, 0, 1), d=0), 2: Hyperplane(Point(0, 1, 0), d=0),
               3: Hyperplane(Point(1, 0, 0), d=0), 4: Hyperplane(Point(1, 1, 0), d=0)}

cones = {1: Cone(1, solutions[1], [-1, -2, -3]), 2: Cone(2, solutions[2], [1, -2, -3]),
         3: Cone(3, solutions[3], [-1, 2, -3]), 4: Cone(4, solutions[4], [1, 2, -3]),
         5: Cone(5, solutions[5], [-1, -2, 3]), 6: Cone(6, solutions[6], [1, -2, 3]),
         7: Cone(7, solutions[7], [-1, 2, 3]), 8: Cone(8, solutions[8], [1, 2, 3])}


def test_intersection():
    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, True)

    assert intersection_lp.dim == 3
    assert intersection_lp.name == 'misc'
    assert intersection_lp.cones == cones
    assert intersection_lp.hyperplanes == hyperplanes
    assert intersection_lp.lp_directory == get_full_path('files', 'lps', 'intersection', 'misc')
    assert intersection_lp.log
    assert file_exists(get_full_path('files', 'lps', 'intersection', 'misc'))


def test_model():
    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, True)
    assert not intersection_lp.test_intersection(Region(), 1, 4)
    assert not intersection_lp.test_intersection(Region(), 2, 4)
    assert not intersection_lp.test_intersection(Region(), 7, 4)
    assert not intersection_lp.test_intersection(Region(), 8, 4)
    assert intersection_lp.test_intersection(Region(), 3, 4)
    assert intersection_lp.test_intersection(Region(), 4, 4)
    assert intersection_lp.test_intersection(Region(), 5, 4)
    assert intersection_lp.test_intersection(Region(), 6, 4)

    assert not intersection_lp.test_intersection(Region(), 1, 1)
    assert not intersection_lp.test_intersection(Region(), 1, 2)
    assert not intersection_lp.test_intersection(Region(), 1, 3)


def test_log():
    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes)
    assert not intersection_lp.log
    assert not intersection_lp.test_intersection(Region(), 1, 1)
    assert not intersection_lp.test_intersection(Region(), 1, 2)
    assert not intersection_lp.test_intersection(Region(), 1, 3)


def test_clear():
    intersection_lp = IntersectionProblem(3, 'misc', cones, hyperplanes, True)
    assert file_exists(get_full_path('files', 'lps', 'intersection', 'misc'))

    intersection_lp.clear_files()
    assert not file_exists(get_full_path('files', 'lps', 'intersection', 'misc'))
