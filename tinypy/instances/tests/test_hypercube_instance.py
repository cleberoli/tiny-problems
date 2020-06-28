import pytest

from tinypy.instances.hypercube_instance import HypercubeInstance


def test_hypercube_instance():
    cub3 = HypercubeInstance(n=3)
    cub6 = HypercubeInstance(n=6)

    cub3_solutions = cub3.get_solution_list()
    cub6_solutions = cub6.get_solution_list()

    assert len(cub3_solutions) == 8     # 2^n
    assert len(cub6_solutions) == 64    # 2^n
    assert cub3.size == 8
    assert cub6.size == 64

    assert cub3_solutions[0].dim == 3  # n
    assert cub6_solutions[0].dim == 6  # n
    assert cub3.dimension == 3
    assert cub6.dimension == 6

    assert list(cub3.get_solution_dict().values()) == cub3_solutions
    assert list(cub6.get_solution_dict().values()) == cub6_solutions


def test_invalid_hypercube_instance():
    with pytest.raises(ValueError):
        HypercubeInstance(n=2)

    with pytest.raises(ValueError):
        HypercubeInstance(size=2)

    with pytest.raises(ValueError):
        HypercubeInstance(size=3)

    with pytest.raises(ValueError):
        HypercubeInstance()
