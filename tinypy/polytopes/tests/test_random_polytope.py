import pytest

from tinypy.polytopes.random_polytope import RandomInstance, RandomPolytope


def test_random_polytope_3_4():
    rnd3_4 = RandomPolytope(3, 4)

    assert rnd3_4.full_name == 'random'
    assert rnd3_4.name == 'rnd'
    assert rnd3_4.dimension == 3
    assert rnd3_4.size == 4
    assert rnd3_4.n == 4
    assert len(rnd3_4.vertices) == 4
    assert rnd3_4.instance.get_solution_dict() == RandomInstance(d=3, m=4).get_solution_dict()


def test_random_polytope_6_8():
    rnd6_8 = RandomPolytope(6, 8)

    assert rnd6_8.full_name == 'random'
    assert rnd6_8.name == 'rnd'
    assert rnd6_8.dimension == 6
    assert rnd6_8.size == 8
    assert rnd6_8.n == 8
    assert len(rnd6_8.vertices) == 8
    assert rnd6_8.instance.get_solution_dict() == RandomInstance(d=6, m=8).get_solution_dict()


def test_invalid_random_polytope():
    with pytest.raises(ValueError):
        RandomPolytope(0, 0)

    with pytest.raises(ValueError):
        RandomPolytope(0, 1)

    with pytest.raises(ValueError):
        RandomPolytope(1, 0)

    with pytest.raises(ValueError):
        RandomPolytope(4, 40)
