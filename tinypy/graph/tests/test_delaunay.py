import pytest

from tinypy.graph.delaunay import DelaunayTriangulation
from tinypy.graph.skeleton import Skeleton


def test_delaunay():
    skeleton = Skeleton()
    delaunay = DelaunayTriangulation(skeleton)
    assert len(delaunay.edges) == 0
    assert len(delaunay.nodes) == 0
    assert isinstance(delaunay.edges, list)
    assert isinstance(delaunay.nodes, list)


def test_add_edge():
    skeleton = Skeleton()
    delaunay = DelaunayTriangulation(skeleton)
    assert len(skeleton.edges) == 0
    assert len(skeleton.nodes) == 0

    delaunay.add_edge(0, 1)
    delaunay.add_edge(0, 1, h=1)
    assert len(delaunay.edges) == 1
    assert len(delaunay.nodes) == 2

    delaunay.add_edge(0, 2, h=2)
    assert len(delaunay.edges) == 2
    assert len(delaunay.nodes) == 3


def test_get_edge():
    skeleton = Skeleton()
    delaunay = DelaunayTriangulation(skeleton)
    delaunay.add_edge(0, 1, h=1)
    delaunay.add_edge(0, 1, h=2)
    delaunay.add_edge(0, 2, h=1)

    assert delaunay.get_edge(0, 1, 'h') == 2
    assert delaunay.get_edge(0, 2, 'h') == 1

    with pytest.raises(KeyError):
        delaunay.get_edge(0, 1, 'p')


def test_get_edges():
    skeleton = Skeleton()
    delaunay = DelaunayTriangulation(skeleton)
    delaunay.add_edge(0, 1, h=2)
    delaunay.add_edge(0, 2, h=1)
    delaunay.add_edge(1, 2, h=3)

    assert len(delaunay.get_edges(0)) == 2
    assert list(delaunay.get_edges(0).keys()) == [1, 2]

    assert len(delaunay.get_edges(1)) == 2
    assert list(delaunay.get_edges(1).keys()) == [0, 2]
