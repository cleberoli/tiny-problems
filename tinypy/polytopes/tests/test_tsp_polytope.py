import pytest

from tinypy.polytopes.tsp_polytope import TSPInstance, TSPPolytope


def test_tsp_polytope_5():
    tsp5 = TSPPolytope(5)

    assert tsp5.full_name == 'travelling salesman'
    assert tsp5.name == 'tsp'
    assert tsp5.dimension == 10
    assert tsp5.size == 12
    assert tsp5.n == 5
    assert len(tsp5.vertices) == 12
    assert tsp5.instance.get_solution_dict() == TSPInstance(n=5).get_solution_dict()


def test_tsp_polytope_6():
    tsp6 = TSPPolytope(6)

    assert tsp6.full_name == 'travelling salesman'
    assert tsp6.name == 'tsp'
    assert tsp6.dimension == 15
    assert tsp6.size == 60
    assert tsp6.n == 6
    assert len(tsp6.vertices) == 60
    assert tsp6.instance.get_solution_dict() == TSPInstance(n=6).get_solution_dict()


def test_invalid_tsp_polytope():
    with pytest.raises(ValueError):
        TSPPolytope(2)
