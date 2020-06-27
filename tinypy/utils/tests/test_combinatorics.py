from tinypy.utils import combinatorics


def test_get_combinations():
    x = [0, 1, 2, 3, 4]
    c0 = combinatorics.get_combinations(x, 0)
    c1 = combinatorics.get_combinations(x, 1)
    c2 = combinatorics.get_combinations(x, 2)
    c3 = combinatorics.get_combinations(x, 3)
    c4 = combinatorics.get_combinations(x, 4)
    c5 = combinatorics.get_combinations(x, 5)

    assert len(c0) == 1
    assert len(c1) == 5
    assert len(c2) == 10
    assert len(c3) == 10
    assert len(c4) == 5
    assert len(c5) == 1

    assert len(c0[0]) == 0
    assert len(c1[0]) == 1
    assert len(c2[0]) == 2
    assert len(c3[0]) == 3
    assert len(c4[0]) == 4
    assert len(c5[0]) == 5


def test_get_permutations():
    x = [0, 1, 2]
    p = combinatorics.get_permutations(x, 2)
    q = combinatorics.get_permutations(x)

    assert len(p) == 9
    assert type(p[0]) is tuple
    assert len(p[0]) == 2

    assert len(q) == 6
    assert type(q[0]) is tuple
    assert len(q[0]) == 3
