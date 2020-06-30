import pytest

from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.point import Point


def test_hyperplane():
    normal = Point(1, 1, 1)
    h1 = Hyperplane(Point(1, 1, 1), p=Point(0, 0, 0))
    h2 = Hyperplane(Point(1, 1, 1), d=0)

    assert h1.normal == normal
    assert h2.normal == normal
    assert h1.d == 0
    assert h2.d == 0


def test_invalid_hyperplane():
    with pytest.raises(ValueError):
        Hyperplane(Point(1, 1, 1))

    with pytest.raises(ValueError):
        Hyperplane(Point(1, 1, 1), p=0)

    with pytest.raises(ValueError):
        Hyperplane(Point(1, 1, 1), d=Point(0, 0, 0))


def test_position():
    h = Hyperplane(Point(1, 1, 1), d=0)
    x = Point(-2, 3, 4)
    y = Point(-2, -3, 4)
    z = Point(5, 2, -7)

    assert h.position(x) > 0
    assert h.position(y) < 0
    assert h.position(z) == 0


def test_in_halfspace():
    h = Hyperplane(Point(1, 1, 1), d=1)
    x = Point(-2, 3, 4)
    y = Point(0, -3, 4)
    z = Point(5, 2, -7)

    assert h.in_halfspace(x)
    assert h.in_halfspace(y)
    assert not h.in_halfspace(z)


def test_neg():
    h1 = Hyperplane(Point(1, 1, 1), d=1)
    h2 = Hyperplane(Point(-1, -1, -1), d=-1)

    assert h1 == -h2


def test_hash():
    h1 = Hyperplane(Point(1, 1, 1), p=Point(0, 0, 0))
    h2 = Hyperplane(Point(1, 1, 1), d=0)
    h3 = Hyperplane(Point(1, 1, 1), d=1)

    assert hash(h1) == hash(h2)
    assert hash(h2) != hash(h3)


def test_get_item():
    h = Hyperplane(Point(1, 2, 3), d=0)

    assert h[0] == 1
    assert h[1] == 2
    assert h[2] == 3


def test_comp():
    h1 = Hyperplane(Point(1, 1, 1), p=Point(0, 0, 0))
    h2 = Hyperplane(Point(1, 1, 1), d=0)
    h3 = Hyperplane(Point(1, 1, 1), d=1)
    h4 = Hyperplane(Point(1, 1, 0), d=0)
    h5 = Hyperplane(Point(1, 1, 2), d=1)

    assert h1 == h2
    assert h1 != h4
    assert h1 < h3
    assert h1 <= h3
    assert h1 > h4
    assert h1 >= h4
    assert h1 < h5


def test_str():
    h = Hyperplane(Point(1, 2, 0, -3, -1), d=0)

    assert str(h) == 'x1 + 2x2 - 3x4 - x5 = 0'


def test_repr():
    h = Hyperplane(Point(1, 2, 0, -3, -1), d=0)

    assert repr(h) == '(1, 2, 0, -3, -1, 0)'
