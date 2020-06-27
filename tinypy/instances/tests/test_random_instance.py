import pytest

from tinypy.instances.random_instance import RandomInstance


def test_random_instance():
    rnd12_5 = RandomInstance(size=12, d=5)
    pyr33_7 = RandomInstance(size=33, d=7)

    rnd12_5_solutions = rnd12_5.get_solution_list()
    pyr33_7_solutions = pyr33_7.get_solution_list()

    assert len(rnd12_5_solutions) == 12     # size
    assert len(pyr33_7_solutions) == 33     # size

    assert rnd12_5_solutions[0].dim == 5    # d
    assert pyr33_7_solutions[0].dim == 7    # d

    assert list(rnd12_5.get_solution_dict().values()) == rnd12_5_solutions
    assert list(pyr33_7.get_solution_dict().values()) == pyr33_7_solutions


def test_invalid_random_instance():
    with pytest.raises(ValueError):
        RandomInstance(n=0)

    with pytest.raises(ValueError):
        RandomInstance(n=1)

    with pytest.raises(ValueError):
        RandomInstance(size=0)

    with pytest.raises(ValueError):
        RandomInstance(size=1)

    with pytest.raises(ValueError):
        RandomInstance(d=0)

    with pytest.raises(ValueError):
        RandomInstance(d=1)

    with pytest.raises(ValueError):
        RandomInstance(size=0, d=0)

    with pytest.raises(ValueError):
        RandomInstance(size=0, d=1)

    with pytest.raises(ValueError):
        RandomInstance(size=1, d=0)

    with pytest.raises(ValueError):
        RandomInstance(size=40, d=4)

    with pytest.raises(ValueError):
        RandomInstance()
