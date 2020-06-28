import pytest

from tinypy.instances.random_instance import RandomInstance


def test_random_instance():
    rnd3_4 = RandomInstance(d=3, m=4)
    rnd6_8 = RandomInstance(d=6, m=8)

    rnd3_4_solutions = rnd3_4.get_solution_list()
    rnd6_8_solutions = rnd6_8.get_solution_list()

    assert rnd3_4.n == 4
    assert rnd6_8.n == 8

    assert len(rnd3_4_solutions) == 4     # size
    assert len(rnd6_8_solutions) == 8     # size
    assert rnd3_4.size == 4
    assert rnd6_8.size == 8

    assert rnd3_4_solutions[0].dim == 3    # d
    assert rnd6_8_solutions[0].dim == 6    # d
    assert rnd3_4.dimension == 3
    assert rnd6_8.dimension == 6

    assert list(rnd3_4.get_solution_dict().values()) == rnd3_4_solutions
    assert list(rnd6_8.get_solution_dict().values()) == rnd6_8_solutions


def test_invalid_random_instance():
    with pytest.raises(ValueError):
        RandomInstance(n=0)

    with pytest.raises(ValueError):
        RandomInstance(n=1)

    with pytest.raises(ValueError):
        RandomInstance(m=0)

    with pytest.raises(ValueError):
        RandomInstance(m=1)

    with pytest.raises(ValueError):
        RandomInstance(d=0)

    with pytest.raises(ValueError):
        RandomInstance(d=1)

    with pytest.raises(ValueError):
        RandomInstance(m=0, d=0)

    with pytest.raises(ValueError):
        RandomInstance(m=0, d=1)

    with pytest.raises(ValueError):
        RandomInstance(m=1, d=0)

    with pytest.raises(ValueError):
        RandomInstance(m=40, d=4)

    with pytest.raises(ValueError):
        RandomInstance()
