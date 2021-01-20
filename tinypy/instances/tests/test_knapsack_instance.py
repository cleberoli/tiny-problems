import pytest

from tinypy.instances.knapsack_instance import KnapsackInstance


def test_knp_instance_3():
    knp3 = KnapsackInstance(n=3, save=False)
    knp3_solutions = knp3.get_solution_list()

    assert knp3.n == 3
    assert knp3.name == '0-KNP-n3'
    assert knp3.type == 'knp'

    assert len(knp3_solutions) == 5
    assert knp3.size == 5

    assert knp3_solutions[0].dim == 3
    assert knp3.dimension == 3

    assert list(knp3.get_solution_dict().values()) == knp3_solutions
    assert list(knp3.get_solution_dict().keys()) == list(range(1, knp3.size + 1))


def test_knp_instance_4():
    knp4 = KnapsackInstance(n=4, origin=False, save=False)
    knp4_solutions = knp4.get_solution_list()

    assert knp4.n == 4
    assert knp4.name == 'KNP-n4'
    assert knp4.type == 'knp'

    assert len(knp4_solutions) == 6
    assert knp4.size == 6

    assert knp4_solutions[0].dim == 4
    assert knp4.dimension == 4

    assert list(knp4.get_solution_dict().values()) == knp4_solutions
    assert list(knp4.get_solution_dict().keys()) == list(range(1, knp4.size + 1))


def test_invalid_knp_instance():
    with pytest.raises(ValueError):
        KnapsackInstance(n=1)

    with pytest.raises(ValueError):
        KnapsackInstance()


def test_generate_solutions():
    assert len(KnapsackInstance(n=3, save=False).generate_solutions()) == 5
    assert len(KnapsackInstance(n=4, origin=False, save=False).generate_solutions()) == 6
