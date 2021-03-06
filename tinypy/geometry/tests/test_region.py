from hashlib import blake2b

from tinypy.geometry.region import Region


def test_region():
    r1 = Region()
    r2 = Region([1, 2])

    assert len(r1.hyperplanes) == 0
    assert len(r2.hyperplanes) == 2


def test_add_hyperplane():
    r = Region()
    assert len(r.hyperplanes) == 0

    r.add_hyperplane(1)
    assert len(r.hyperplanes) == 1
    assert r.hyperplanes == [1]

    r.add_hyperplane(-2)
    assert len(r.hyperplanes) == 2
    assert r.hyperplanes == [1, -2]


def test_union():
    r = Region([1, 2])
    assert len(r.hyperplanes) == 2
    assert r.hyperplanes == [1, 2]

    r = r.union(Region([2, 3]))
    assert len(r.hyperplanes) == 3
    assert r.hyperplanes == [1, 2, 3]

    r = r.union(Region([4]))
    assert len(r.hyperplanes) == 4
    assert r.hyperplanes == [1, 2, 3, 4]

    r = r.union(Region([-2]))
    assert len(r.hyperplanes) == 5
    assert r.hyperplanes == [1, 2, -2, 3, 4]


def test_str():
    r = Region([2, 1])

    assert str(r) == '[1, 2]'


def test_repr():
    r = Region([1, -2])
    h = blake2b(digest_size=20)
    h.update(b'[1, -2]')

    assert repr(r) == h.hexdigest()
