import pytest

from tinypy.polytopes.hypercube_polytope import HypercubeInstance, HypercubePolytope


def test_hypercube_polytope_3():
    cub3 = HypercubePolytope(3)

    assert cub3.full_name == 'hypercube'
    assert cub3.name == 'cub'
    assert cub3.dimension == 3
    assert cub3.size == 8
    assert cub3.n == 3
    assert len(cub3.vertices) == 8
    assert cub3.instance.get_solution_dict() == HypercubeInstance(n=3).get_solution_dict()

    assert cub3.get_bisector(1, 2) == 1
    assert cub3.get_bisector(1, 4) == 5


def test_hypercube_polytope_6():
    cub6 = HypercubePolytope(6)

    assert cub6.full_name == 'hypercube'
    assert cub6.name == 'cub'
    assert cub6.dimension == 6
    assert cub6.size == 64
    assert cub6.n == 6
    assert len(cub6.vertices) == 64
    assert cub6.instance.get_solution_dict() == HypercubeInstance(n=6).get_solution_dict()


def test_invalid_hypercube_polytope():
    with pytest.raises(ValueError):
        HypercubePolytope(2)
