import pytest

from tinypy.graph.kn import Kn


def test_kn():
    k5 = Kn(5)
    k10 = Kn(10)

    assert k5.n == 5
    assert k10.n == 10

    assert len(k5.nodes) == 5       # n
    assert k5.nodes[0] == 1
    assert k5.nodes[4] == 5
    assert len(k10.nodes) == 10     # n
    assert k10.nodes[0] == 1
    assert k10.nodes[9] == 10

    assert len(k5.edges) == 10      # n*(n-1)/2
    assert k5.edges[0] == '1-2'
    assert k5.edges[4] == '2-3'
    assert k5.edges[9] == '4-5'
    assert len(k10.edges) == 45     # n*(n-1)/2
    assert k10.edges[0] == '1-2'
    assert k10.edges[9] == '2-3'
    assert k10.edges[44] == '9-10'


def test_get_hamilton_cycles():
    k5 = Kn(5)
    k6 = Kn(6)
    cycles5 = k5.get_hamilton_cycles()
    cycles6 = k6.get_hamilton_cycles()

    assert len(cycles5) == 12       # (n-1)!/2
    assert len(cycles6) == 60       # (n-1)!/2

    assert cycles5[0].coords == (0, 0, 1, 1, 1, 0, 1, 1, 0, 0)
    assert cycles5[4].coords == (0, 1, 1, 0, 0, 1, 1, 0, 1, 0)
    assert cycles5[11].coords == (1, 1, 0, 0, 0, 1, 0, 0, 1, 1)

    assert cycles6[0].coords == (0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0)
    assert cycles6[10].coords == (0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1)
    assert cycles6[59].coords == (1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1)


def test_get_cuts():
    k5 = Kn(5)
    k6 = Kn(6)
    cuts5 = k5.get_cuts()
    cuts6 = k6.get_cuts()

    assert len(cuts5) == 16         # 2^(n-1)
    assert len(cuts6) == 32         # 2^(n-1)

    assert cuts5[0].coords == (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    assert cuts5[4].coords == (0, 1, 0, 0, 1, 0, 0, 1, 1, 0)
    assert cuts5[15].coords == (1, 1, 1, 1, 0, 0, 0, 0, 0, 0)

    assert cuts6[0].coords == (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    assert cuts6[10].coords == (0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1)
    assert cuts6[31].coords == (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


def test_get_triangles():
    k5 = Kn(5)
    k6 = Kn(6)
    k5_triangles = k5.get_triangles()
    k6_triangles = k6.get_triangles()

    assert len(k5_triangles) == 10  # C(n, 3)
    assert len(k6_triangles) == 20  # C(n, 3)

    assert k5_triangles[0] == [0, 1, 4]
    assert k5_triangles[4] == [1, 3, 8]
    assert k5_triangles[9] == [7, 8, 9]

    assert k6_triangles[0] == [0, 1, 5]
    assert k6_triangles[9] == [3, 4, 14]
    assert k6_triangles[19] == [12, 13, 14]


def test_invalid_kn():
    with pytest.raises(ValueError):
        Kn(2)
