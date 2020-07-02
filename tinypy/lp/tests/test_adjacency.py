from tinypy.lp.adjacency import AdjacencyProblem
from tinypy.geometry.point import Point
from tinypy.utils.file import file_exists, get_full_path

p = {1: Point(1, 0, 0), 2: Point(0, 1, 0), 3: Point(0, 0, 1)}


def test_adjacency():
    adjacency_lp = AdjacencyProblem(3, 'misc', p)

    assert adjacency_lp.dim == 3
    assert adjacency_lp.name == 'misc'
    assert adjacency_lp.p == p
    assert adjacency_lp.lp_directory == get_full_path('files', 'lps', 'adjacency', 'misc')
    assert not adjacency_lp.log
    assert file_exists(get_full_path('files', 'lps', 'adjacency', 'misc'))


def test_primal():
    adjacency_lp = AdjacencyProblem(3, 'misc', p, True)
    assert adjacency_lp.test_edge_primal(1, 2)
    assert adjacency_lp.test_edge_primal(1, 3)
    assert adjacency_lp.test_edge_primal(2, 3)
    assert adjacency_lp.test_edge_primal(2, 3)


def test_dual():
    adjacency_lp = AdjacencyProblem(3, 'misc', p, True)
    assert adjacency_lp.test_edge_dual(1, 2)
    assert adjacency_lp.test_edge_dual(1, 3)
    assert adjacency_lp.test_edge_dual(2, 3)
    assert adjacency_lp.test_edge_dual(2, 3)


def test_log():
    adjacency_lp = AdjacencyProblem(3, 'misc', p, True)
    assert adjacency_lp.test_edge_primal(1, 2)
    assert adjacency_lp.test_edge_primal(1, 3)
    assert adjacency_lp.test_edge_dual(2, 3)
    assert adjacency_lp.test_edge_dual(2, 3)


def test_clear():
    adjacency_lp = AdjacencyProblem(3, 'misc', p)
    assert file_exists(get_full_path('files', 'lps', 'adjacency', 'misc'))

    adjacency_lp.clear_files()
    assert not file_exists(get_full_path('files', 'lps', 'adjacency', 'misc'))

