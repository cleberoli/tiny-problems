import pytest

from tinypy.instances.cut_instance import CutInstance


def test_cut_instance_5():
    cut5 = CutInstance(n=5)
    cut5_solutions = cut5.get_solution_list()

    assert cut5.n == 5
    assert cut5.name == 'CUT-n5'
    assert cut5.type == 'cut'

    assert len(cut5_solutions) == 16        # 2^(n-1)
    assert cut5.size == 16

    assert cut5_solutions[0].dim == 10      # n*(n-1)/2
    assert cut5.dimension == 10

    assert list(cut5.get_solution_dict().values()) == cut5_solutions
    assert list(cut5.get_solution_dict().keys()) == list(range(1, cut5.size + 1))


def test_cut_instance_6():
    cut6 = CutInstance(n=6)
    cut6_solutions = cut6.get_solution_list()

    assert cut6.n == 6
    assert cut6.name == 'CUT-n6'
    assert cut6.type == 'cut'

    assert len(cut6_solutions) == 32        # 2^(n-1)
    assert cut6.size == 32

    assert cut6_solutions[0].dim == 15      # n*(n-1)/2
    assert cut6.dimension == 15

    assert list(cut6.get_solution_dict().values()) == cut6_solutions
    assert list(cut6.get_solution_dict().keys()) == list(range(1, cut6.size + 1))


def test_invalid_cut_instance():
    with pytest.raises(ValueError):
        CutInstance(n=2)

    with pytest.raises(ValueError):
        CutInstance(size=2)

    with pytest.raises(ValueError):
        CutInstance(size=3)

    with pytest.raises(ValueError):
        CutInstance()


def test_generate_solutions():
    assert len(CutInstance(n=5).generate_solutions()) == 16
    assert len(CutInstance(n=6).generate_solutions()) == 32
