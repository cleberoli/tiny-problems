from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.point import Point
from tinypy.geometry.region import Region


def test_region():
    r1 = Region(3)
    r2 = Region(3, {0: Hyperplane(Point(1, 1, 1), d=0), 1: Hyperplane(Point(1, 1, 1), d=1)})

    assert r1.dim == 3
    assert len(r1.hyperplanes) == 0

    assert r2.dim == 3
    assert len(r2.hyperplanes) == 2


def test_add_hyperplane():
    r = Region(3)
    assert r.dim == 3
    assert len(r.hyperplanes) == 0

    r.add_hyperplane(0, Hyperplane(Point(1, 1, 1), d=0))
    assert r.dim == 3
    assert len(r.hyperplanes) == 1
    assert r.hyperplanes[0] == Hyperplane(Point(1, 1, 1), d=0)


def test_union():
    r = Region(3, {0: Hyperplane(Point(1, 1, 1), d=0), 1: Hyperplane(Point(1, 1, 1), d=1)})
    assert r.dim == 3
    assert len(r.hyperplanes) == 2

    r = r.union(Region(3, {2: Hyperplane(Point(1, 1, 1), d=2), 3: Hyperplane(Point(1, 1, 1), d=3)}))
    assert r.dim == 3
    assert len(r.hyperplanes) == 4


def test_str():
    r = Region(3, {0: Hyperplane(Point(1, 1, 1), d=0), 1: Hyperplane(Point(1, 1, 1), d=1)})

    assert str(r) == '{0: x1 + x2 + x3 = 0, 1: x1 + x2 + x3 = 1}'


def test_repr():
    r = Region(3, {0: Hyperplane(Point(1, 1, 1), d=0), 1: Hyperplane(Point(1, 1, 1), d=1)})

    assert repr(r) == '{0: (1, 1, 1, 0), 1: (1, 1, 1, 1)}'
