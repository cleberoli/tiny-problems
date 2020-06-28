import pytest

from tinypy.geometry.point import Point


def test_point():
    p0 = Point(0)
    p1 = Point(0, 0)
    p2 = Point(0, 0, 0)
    p3 = Point(0, 0, 0, 0)
    p4 = Point([0, 0, 0, 0, 0])
    p5 = Point((0, 0, 0, 0, 0, 0))
    p6 = Point((0, 0, 0, 0, 0, 0), 0, 0)

    assert p0.dim == 1
    assert p1.dim == 2
    assert p2.dim == 3
    assert p3.dim == 4
    assert p4.dim == 5
    assert p5.dim == 6
    assert p6.dim == 6

    assert p0.coords == (0,)
    assert p1.coords == (0, 0)
    assert p2.coords == (0, 0, 0)
    assert p3.coords == (0, 0, 0, 0)
    assert p4.coords == (0, 0, 0, 0, 0)
    assert p5.coords == (0, 0, 0, 0, 0, 0)
    assert p6.coords == (0, 0, 0, 0, 0, 0)


def test_invalid_point():
    with pytest.raises(ValueError):
        Point('0000')

    with pytest.raises(ValueError):
        Point('0', '1')

    with pytest.raises(ValueError):
        Point(['0', '1'])

    with pytest.raises(ValueError):
        Point(('0', '1'))


def test_origin():
    p = Point(0, 0, 0, 0)
    origin = Point.origin(4)

    assert origin.dim == p.dim
    assert origin == p


def test_random():
    p = Point.random(5)

    assert p.dim == 5
    assert all([0 <= x <= 1 for x in p.coords])

    p = Point.random(8, -2, 5)

    assert p.dim == 8
    assert all([-2 <= x <= 5 for x in p.coords])


def test_homogeneous_coords():
    x = Point(3, 4)

    assert len(x.homogeneous_coords) == 3
    assert x.homogeneous_coords == (3, 4, 1)


def test_norm():
    x = Point(3, 4)
    y = Point(-3, -4)

    assert x.norm == 5
    assert y.norm == 5


def test_distance():
    x = Point(3, 4)
    y = Point(6, 8)
    z = Point(1, 2, 3)

    assert x.distance(y) == 5
    assert y.distance(x) == 5

    with pytest.raises(ValueError):
        x.distance(z)


def test_add_coord():
    x = Point(3, 4)
    assert x.coords == (3, 4)
    assert x.dim == 2

    x.add_coord(1)
    assert x.coords == (3, 4, 1)
    assert x.dim == 3

    with pytest.raises(ValueError):
        x.add_coord(5.5)


def test_add():
    x = Point(1, 2, 3)
    y = Point(4.5, 3.5, 2.5)
    z = Point(1, 2)
    p = Point(5.5, 5.5, 5.5)

    assert x + y == p
    assert y + x == p

    with pytest.raises(ValueError):
        x + z


def test_sub():
    x = Point(1, 2, 3)
    y = Point(4.5, 3.5, 2.5)
    z = Point(1, 2)
    p = Point(-3.5, -1.5, 0.5)

    assert x - y == p
    assert y - x == -p

    with pytest.raises(ValueError):
        x - z


def test_mul():
    x = Point(1, 2, 3)
    p = Point(2, 4, 6)

    assert 2 * x == p
    assert x * 2 == p

    with pytest.raises(ValueError):
        x * 'a'


def test_dot():
    x = Point(3, 4)
    y = Point(6, 8)
    z = Point(1, 2, 3)

    assert x * y == 50
    assert y * x == 50

    with pytest.raises(ValueError):
        x * z


def test_neg():
    x = Point(1, 0, -1)
    y = Point(-1, 0, 1)

    assert x == -y


def test_get_item():
    p = Point(1, 2, 3)

    assert p[0] == 1
    assert p[1] == 2
    assert p[2] == 3


def test_hash():
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(2, 3)

    assert hash(p1) == hash(p2)
    assert hash(p1) != hash(p3)


def test_comp():
    p1 = Point(1, 2, 3)
    p2 = Point(1, 2, 3)
    p3 = Point(2, 3, 4)
    p4 = Point(1, 2, 3, 4)

    assert p1 == p2
    assert p1 < p3
    assert p4 > p2
    assert p3 > p4
    assert p2 != p3


def test_str():
    p = Point(1, 2, 3)

    assert str(p) == '(1, 2, 3)'


def test_repr():
    p = Point(1, 2, 3)

    assert repr(p) == '(1, 2, 3)'
