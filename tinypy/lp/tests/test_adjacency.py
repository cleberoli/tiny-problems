from tinypy.lp.adjacency import AdjacencyProblem
from tinypy.geometry.point import Point

p = {1: Point(1, 0, 0), 2: Point(0, 1, 0), 3: Point(0, 0, 1)}


def test_adjacency():
    adjacency_lp = AdjacencyProblem(3, 'misc', p)

    assert adjacency_lp.dim == 3
    assert adjacency_lp.name == 'misc'
    assert adjacency_lp.p == p


def test_primal():
    adjacency_lp = AdjacencyProblem(3, 'misc', p)
    assert adjacency_lp.test_edge_primal(1, 2)
    assert adjacency_lp.test_edge_primal(1, 3)
    assert adjacency_lp.test_edge_primal(2, 3)
    assert adjacency_lp.test_edge_primal(2, 3)


def test_dual():
    adjacency_lp = AdjacencyProblem(3, 'misc', p)
    assert adjacency_lp.test_edge_dual(1, 2)
    assert adjacency_lp.test_edge_dual(1, 3)
    assert adjacency_lp.test_edge_dual(2, 3)
    assert adjacency_lp.test_edge_dual(2, 3)

