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

