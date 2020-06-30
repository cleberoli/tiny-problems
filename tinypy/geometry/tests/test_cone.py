from tinypy.geometry.cone import Cone
from tinypy.geometry.point import Point


def test_cone():
    hyperplanes = [1, 2]
    cone = Cone(0, Point(0, 0, 0), hyperplanes)

    assert cone.tag == 0
    assert cone.solution == Point(0, 0, 0)
    assert cone.hyperplanes == hyperplanes
