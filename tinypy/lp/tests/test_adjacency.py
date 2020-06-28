from tinypy.lp.adjacency import AdjacencyProblem
from tinypy.geometry.point import Point
from tinypy.utils.file import file_exists, get_full_path

p = {0: Point(1, 0, 0), 1: Point(0, 1, 0), 2: Point(0, 0, 1)}


def test_adjacency():
    adjacency_lp = AdjacencyProblem(3, 'misc', p)

    assert adjacency_lp.dim == 3
    assert adjacency_lp.name == 'misc'
    assert adjacency_lp.p == p
    assert adjacency_lp.lp_directory == get_full_path('lp', 'adjacency', 'misc')
    assert adjacency_lp.log
    assert file_exists(get_full_path('lp', 'adjacency', 'misc'))


def test_primal():
    adjacency_lp = AdjacencyProblem(3, 'misc', p)
    assert adjacency_lp.test_edge_primal(0, 1)
    assert adjacency_lp.test_edge_primal(0, 2)
    assert adjacency_lp.test_edge_primal(1, 2)
    assert adjacency_lp.test_edge_primal(1, 2)


def test_dual():
    adjacency_lp = AdjacencyProblem(3, 'misc', p)
    assert adjacency_lp.test_edge_dual(0, 1)
    assert adjacency_lp.test_edge_dual(0, 2)
    assert adjacency_lp.test_edge_dual(1, 2)
    assert adjacency_lp.test_edge_dual(1, 2)


def test_clear():
    adjacency_lp = AdjacencyProblem(3, 'misc', p)
    assert file_exists(get_full_path('lp', 'adjacency', 'misc'))

    adjacency_lp.clear_files()
    assert not file_exists(get_full_path('lp', 'adjacency', 'misc'))

