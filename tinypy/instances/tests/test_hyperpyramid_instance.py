import pytest

from tinypy.instances.hyperpyramid_instance import HyperpyramidInstance


def test_hyperpyramid_instance():
    pyr3 = HyperpyramidInstance(n=3)
    pyr6 = HyperpyramidInstance(n=6)

    pyr3_solutions = pyr3.get_solution_list()
    pyr6_solutions = pyr6.get_solution_list()

    assert len(pyr3_solutions) == 5     # 2^(n-1) + 1
    assert len(pyr6_solutions) == 33    # 2^(n-1) + 1

    assert pyr3_solutions[0].dim == 3  # n
    assert pyr6_solutions[0].dim == 6  # n

    assert list(pyr3.get_solution_dict().values()) == pyr3_solutions
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
