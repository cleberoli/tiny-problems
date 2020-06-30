import pytest

from tinypy.polytopes.random_polytope import RandomInstance, RandomPolytope
from tinypy.utils.file import delete_file, file_exists, get_full_path


def test_random_polytope_3_4():
    rnd3_4 = RandomPolytope(3, 4)

    assert rnd3_4.full_name == 'random'
    assert rnd3_4.name == 'rnd'
    assert rnd3_4.dimension == 3
    assert rnd3_4.size == 4
    assert rnd3_4.n == 4
    assert len(rnd3_4.vertices) == 4
    assert rnd3_4.instance.get_solution_dict() == RandomInstance(d=3, m=4).get_solution_dict()


def test_random_polytope_6_8():
    rnd6_8 = RandomPolytope(6, 8)

    assert rnd6_8.full_name == 'random'
    assert rnd6_8.name == 'rnd'
    assert rnd6_8.dimension == 6
    assert rnd6_8.size == 8
    assert rnd6_8.n == 8
    assert len(rnd6_8.vertices) == 8
    assert rnd6_8.instance.get_solution_dict() == RandomInstance(d=6, m=8).get_solution_dict()


def test_invalid_random_polytope():
    with pytest.raises(ValueError):
        RandomPolytope(0, 0)

    with pytest.raises(ValueError):
        RandomPolytope(0, 1)

    with pytest.raises(ValueError):
        RandomPolytope(1, 0)

    with pytest.raises(ValueError):
        RandomPolytope(4, 40)


def test_new_random_polytope():
    instance_file = get_full_path('files', 'instances', 'rnd', 'RND-d40-m4.tpif')
    skeleton_file = get_full_path('files', 'skeletons', 'rnd', 'RND-d40-m4.tpsf')
    cone_file = get_full_path('files', 'cones', 'rnd', 'RND-d40-m4.tpcf')

    assert not file_exists(instance_file)
    assert not file_exists(skeleton_file)
    assert not file_exists(cone_file)

    RandomPolytope(40, 4)
    assert file_exists(instance_file)
    assert file_exists(skeleton_file)
    assert file_exists(cone_file)

    delete_file(instance_file)
    delete_file(skeleton_file)
    delete_file(cone_file)

    assert not file_exists(instance_file)
    assert not file_exists(skeleton_file)
    assert not file_exists(cone_file)
