import pytest

from tinypy.instances.cut_instance import CutInstance


def test_cut_instance():
    cut5 = CutInstance(n=5)
    cut6 = CutInstance(n=6)

    cut5_solutions = cut5.get_solution_list()
    cut6_solutions = cut6.get_solution_list()

    assert cut5.n == 5
    assert cut6.n == 6

    assert len(cut5_solutions) == 16        # 2^(n-1)
    assert len(cut6_solutions) == 32        # 2^(n-1)
    assert cut5.size == 16
    assert cut6.size == 32

    assert cut5_solutions[0].dim == 10      # n*(n-1)/2
    assert cut6_solutions[0].dim == 15      # n*(n-1)/2
    assert cut5.dimension == 10
    assert cut6.dimension == 15

    assert list(cut5.get_solution_dict().values()) == cut5_solutions
    assert list(cut6.get_solution_dict().values()) == cut6_solutions


def test_invalid_cut_instance():
    with pytest.raises(ValueError):
        CutInstance(n=2)

    with pytest.raises(ValueError):
        CutInstance(size=2)

    with pytest.raises(ValueError):
        CutInstance(size=3)

    with pytest.raises(ValueError):
        CutInstance()
