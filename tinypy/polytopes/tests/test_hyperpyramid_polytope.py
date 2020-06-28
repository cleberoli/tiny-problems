import pytest

from tinypy.polytopes.hyperpyramid_polytope import HyperpyramidInstance, HyperpyramidPolytope


def test_hyperpyramid_polytope_3():
    pyr3 = HyperpyramidPolytope(3)

    assert pyr3.full_name == 'hyperpyramid'
    assert pyr3.name == 'pyr'
    assert pyr3.dimension == 3
    assert pyr3.size == 5
    assert pyr3.n == 3
    assert len(pyr3.vertices) == 5
    assert pyr3.instance.get_solution_dict() == HyperpyramidInstance(n=3).get_solution_dict()


def test_hyperpyramid_polytope_6():
    pyr6 = HyperpyramidPolytope(6)

    assert pyr6.full_name == 'hyperpyramid'
    assert pyr6.name == 'pyr'
    assert pyr6.dimension == 6
    assert pyr6.size == 33
    assert pyr6.n == 6
    assert len(pyr6.vertices) == 33
    assert pyr6.instance.get_solution_dict() == HyperpyramidInstance(n=6).get_solution_dict()


def test_invalid_hyperpyramid_polytope():
    with pytest.raises(ValueError):
        HyperpyramidPolytope(2)
