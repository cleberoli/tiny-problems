import pytest

from tinypy.instances.hyperpyramid_instance import HyperpyramidInstance


def test_hyperpyramid_instance_3():
    pyr3 = HyperpyramidInstance(n=3)
    pyr3_solutions = pyr3.get_solution_list()

    assert pyr3.n == 3
    assert pyr3.name == 'PYR-n3'
    assert pyr3.type == 'pyr'

    assert len(pyr3_solutions) == 5     # 2^(n-1) + 1
    assert pyr3.size == 5

    assert pyr3_solutions[0].dim == 3  # n
    assert pyr3.dimension == 3

    assert list(pyr3.get_solution_dict().values()) == pyr3_solutions


def test_hyperpyramid_instance_6():
    pyr6 = HyperpyramidInstance(n=6)
    pyr6_solutions = pyr6.get_solution_list()

    assert pyr6.n == 6
    assert pyr6.name == 'PYR-n6'
    assert pyr6.type == 'pyr'

    assert len(pyr6_solutions) == 33    # 2^(n-1) + 1
    assert pyr6.size == 33

    assert pyr6_solutions[0].dim == 6  # n
    assert pyr6.dimension == 6

    assert list(pyr6.get_solution_dict().values()) == pyr6_solutions


def test_invalid_hyperpyramid_instance():
    with pytest.raises(ValueError):
        HyperpyramidInstance(n=2)

    with pytest.raises(ValueError):
        HyperpyramidInstance(size=2)

    with pytest.raises(ValueError):
        HyperpyramidInstance(size=3)

    with pytest.raises(ValueError):
        HyperpyramidInstance()
