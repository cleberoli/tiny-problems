import pytest

from tinypy.polytopes.knapsack_polytope import KnapsackInstance, KnapsackPolytope


def test_knp_polytope_3():
    knp3 = KnapsackPolytope(3, origin=True, save=False)

    assert knp3.full_name == 'knapsack'
    assert knp3.name == 'knp'
    assert knp3.dimension == 3
    assert knp3.size == 5
    assert knp3.n == 3
    assert len(knp3.vertices) == 5
    assert knp3.instance.get_solution_dict() == KnapsackInstance(n=3, origin=True, save=False).get_solution_dict()


def test_knp_polytope_4():
    knp4 = KnapsackPolytope(4, origin=False, save=False)

    assert knp4.full_name == 'knapsack'
    assert knp4.name == 'knp'
    assert knp4.dimension == 4
    assert knp4.size == 6
    assert knp4.n == 4
    assert len(knp4.vertices) == 6
    assert knp4.instance.get_solution_dict() == KnapsackInstance(n=4, origin=False, save=False).get_solution_dict()


def test_invalid_knp_polytope():
    with pytest.raises(ValueError):
        KnapsackPolytope(1)
