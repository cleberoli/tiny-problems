import pytest

from tinypy.instances.tsp_instance import TSPInstance


def test_tsp_instance_5():
    tsp5 = TSPInstance(n=5)
    tsp5_solutions = tsp5.get_solution_list()

    assert tsp5.n == 5
    assert tsp5.name == 'TSP-n5'
    assert tsp5.type == 'tsp'

    assert len(tsp5_solutions) == 12        # (n-1)!/2
    assert tsp5.size == 12

    assert tsp5_solutions[0].dim == 10      # n*(n-1)/2
    assert tsp5.dimension == 10

    assert list(tsp5.get_solution_dict().values()) == tsp5_solutions


def test_tsp_instance_6():
    tsp6 = TSPInstance(n=6)
    tsp6_solutions = tsp6.get_solution_list()

    assert tsp6.n == 6
    assert tsp6.name == 'TSP-n6'
    assert tsp6.type == 'tsp'

    assert len(tsp6_solutions) == 60        # (n-1)!/2
    assert tsp6.size == 60

    assert tsp6_solutions[0].dim == 15      # n*(n-1)/2
    assert tsp6.dimension == 15

    assert list(tsp6.get_solution_dict().values()) == tsp6_solutions


def test_invalid_tsp_instance():
    with pytest.raises(ValueError):
        TSPInstance(n=2)

    with pytest.raises(ValueError):
        TSPInstance(size=2)

    with pytest.raises(ValueError):
        TSPInstance(size=3)

    with pytest.raises(ValueError):
        TSPInstance()


def test_generate_solutions():
    assert len(TSPInstance(n=5).generate_solutions()) == 12
    assert len(TSPInstance(n=6).generate_solutions()) == 60
