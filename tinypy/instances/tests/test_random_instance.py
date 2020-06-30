import pytest

from tinypy.instances.random_instance import RandomInstance
from tinypy.utils.file import delete_file, file_exists, get_full_path


def test_random_instance_3_4():
    rnd3_4 = RandomInstance(d=3, m=4)
    rnd3_4_solutions = rnd3_4.get_solution_list()

    assert rnd3_4.n == 4
    assert rnd3_4.name == 'RND-d3-m4'
    assert rnd3_4.type == 'rnd'

    assert len(rnd3_4_solutions) == 4     # size
    assert rnd3_4.size == 4

    assert rnd3_4_solutions[0].dim == 3    # d
    assert rnd3_4.dimension == 3

    assert list(rnd3_4.get_solution_dict().values()) == rnd3_4_solutions
    assert list(rnd3_4.get_solution_dict().keys()) == list(range(1, rnd3_4.size + 1))


def test_random_instance_6_8():
    rnd6_8 = RandomInstance(d=6, m=8)
    rnd6_8_solutions = rnd6_8.get_solution_list()

    assert rnd6_8.n == 8
    assert rnd6_8.name == 'RND-d6-m8'
    assert rnd6_8.type == 'rnd'

    assert len(rnd6_8_solutions) == 8     # size
    assert rnd6_8.size == 8

    assert rnd6_8_solutions[0].dim == 6    # d
    assert rnd6_8.dimension == 6

    assert list(rnd6_8.get_solution_dict().values()) == rnd6_8_solutions
    assert list(rnd6_8.get_solution_dict().keys()) == list(range(1, rnd6_8.size + 1))


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
        RandomInstance(d=0, m=0)

    with pytest.raises(ValueError):
        RandomInstance(d=0, m=1)

    with pytest.raises(ValueError):
        RandomInstance(d=1, m=0)

    with pytest.raises(ValueError):
        RandomInstance(d=4, m=40)

    with pytest.raises(ValueError):
        RandomInstance()


def test_new_random_instance():
    instance_file = get_full_path('files', 'instances', 'rnd', 'RND-d40-m4.tpif')
    assert not file_exists(instance_file)

    RandomInstance(d=40, m=4)
    assert file_exists(instance_file)

    delete_file(instance_file)
    assert not file_exists(instance_file)


def test_generate_solutions():
    assert len(RandomInstance(d=3, m=4).generate_solutions()) == 4
    assert len(RandomInstance(d=6, m=8).generate_solutions()) == 8
