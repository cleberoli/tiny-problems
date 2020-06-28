import pytest

from tinypy.instances.tsp_instance import TSPInstance


def test_cut_instance():
    tsp5 = TSPInstance(n=5)
    tsp6 = TSPInstance(n=6)

    tsp5_solutions = tsp5.get_solution_list()
    tsp6_solutions = tsp6.get_solution_list()

    assert len(tsp5_solutions) == 12        # (n-1)!/2
    assert len(tsp6_solutions) == 60        # (n-1)!/2
    assert tsp5.size == 12
    assert tsp6.size == 60

    assert tsp5_solutions[0].dim == 10      # n*(n-1)/2
    assert tsp6_solutions[0].dim == 15      # n*(n-1)/2
    assert tsp5.dimension == 10
    assert tsp6.dimension == 15

    assert list(tsp5.get_solution_dict().values()) == tsp5_solutions
    assert list(tsp6.get_solution_dict().values()) == tsp6_solutions


def test_invalid_cut_instance():
    with pytest.raises(ValueError):
        TSPInstance(n=2)

    with pytest.raises(ValueError):
        TSPInstance(size=2)

    with pytest.raises(ValueError):
        TSPInstance(size=3)

    with pytest.raises(ValueError):
        TSPInstance()
