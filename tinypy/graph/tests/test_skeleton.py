import pytest

from tinypy.graph.skeleton import Skeleton


def test_skeleton():
    skeleton = Skeleton()
    assert len(skeleton.edges) == 0
    assert len(skeleton.nodes) == 0
    assert isinstance(skeleton.edges, list)
    assert isinstance(skeleton.nodes, list)


def test_add_edge():
    skeleton = Skeleton()
    assert len(skeleton.edges) == 0
    assert len(skeleton.nodes) == 0

    skeleton.add_edge(0, 1)
    skeleton.add_edge(0, 1, h=1)
    assert len(skeleton.edges) == 1
    assert len(skeleton.nodes) == 2

    skeleton.add_edge(0, 2, h=2)
    assert len(skeleton.edges) == 2
    assert len(skeleton.nodes) == 3


def test_get_edge():
    skeleton = Skeleton()
    skeleton.add_edge(0, 1, h=1)
    skeleton.add_edge(0, 1, h=2)
    skeleton.add_edge(0, 2, h=1)

    assert skeleton.get_edge(0, 1, 'h') == 2
    assert skeleton.get_edge(0, 2, 'h') == 1

    with pytest.raises(KeyError):
        skeleton.get_edge(0, 1, 'p')


def test_get_edges():
    skeleton = Skeleton()
    skeleton.add_edge(0, 1, h=2)
    skeleton.add_edge(0, 2, h=1)
    skeleton.add_edge(1, 2, h=3)

    assert len(skeleton.get_edges(0)) == 2
    assert list(skeleton.get_edges(0).keys()) == [1, 2]

    assert len(skeleton.get_edges(1)) == 2
    assert list(skeleton.get_edges(1).keys()) == [0, 2]
