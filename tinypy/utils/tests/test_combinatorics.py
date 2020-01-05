from tinypy.utils import combinatorics


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

