import pytest
from tinypy.geometry import Point


def test_point():
    p1 = Point(0, 0)
    p2 = Point(0, 0, 0)
    p3 = Point(0, 0, 0, 0)
    p4 = Point([0, 0, 0, 0, 0])
    p5 = Point((0, 0, 0, 0, 0, 0))

    assert p1.dim == 2
    assert p2.dim == 3
    assert p3.dim == 4
    assert p4.dim == 5
    assert p5.dim == 6


def test_invalid_points():
    with pytest.raises(ValueError):
        Point('0000')


def test_origin():
    p = Point(0, 0, 0, 0)
    origin = p.origin

    assert origin.dim == p.dim
    assert origin == p


def test_add():
    x = Point(1, 2, 3)
    y = Point(4.5, 3.5, 2.5)
    p = Point(5.5, 5.5, 5.5)

    assert x + y == p
    assert y + x == p


def test_sub():
    x = Point(1, 2, 3)
    y = Point(4.5, 3.5, 2.5)
    p = Point(-3.5, -1.5, 0.5)

    assert x - y == p
    assert y - x == -p


def test_mul():
    x = Point(1, 2, 3)
    p = Point(2, 4, 6)

    assert 2 * x == p
    assert x * 2 == p


def test_distance():
    x = Point(3, 4)
    y = Point(6, 8)

    assert x.distance(y) == 5
    assert y.distance(x) == 5


def test_norm():
    x = Point(3, 4)

    assert x.norm == 5


def test_dot():
    x = Point(3, 4)
    y = Point(6, 8)

    assert x * y == 50
    assert y * x == 50
