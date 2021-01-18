import pytest

from tinypy.polytopes.cut_polytope import CutInstance, CutPolytope


def test_cut_polytope_5():
    cut5 = CutPolytope(5)

    assert cut5.full_name == 'cut'
    assert cut5.name == 'cut'
    assert cut5.dimension == 10
    assert cut5.size == 15
    assert cut5.n == 5
    assert len(cut5.vertices) == 15
    assert cut5.instance.get_solution_dict() == CutInstance(n=5).get_solution_dict()


def test_cut_polytope_6():
    cut6 = CutPolytope(6)

    assert cut6.full_name == 'cut'
    assert cut6.name == 'cut'
    assert cut6.dimension == 15
    assert cut6.size == 31
    assert cut6.n == 6
    assert len(cut6.vertices) == 31
    assert cut6.instance.get_solution_dict() == CutInstance(n=6).get_solution_dict()


def test_invalid_cut_polytope():
    with pytest.raises(ValueError):
        CutPolytope(2)
