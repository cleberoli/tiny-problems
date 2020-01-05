import pytest

from tinypy.geometry import Point
from tinypy.polytopes import Hyperpyramid


def test_invalid_hyperpyramid():
    with pytest.raises(ValueError):
        Hyperpyramid(2)


def test_get_vertices_3():
    pyramid = Hyperpyramid(3)
    expected_vertices = [(0, 0, 0), (0, 2, 0), (2, 0, 0), (2, 2, 0), (1, 1, 1)]

    assert len(pyramid.vertices) == 5
    assert all([a == Point(b) for a, b in zip(pyramid.vertices, expected_vertices)])


def test_get_vertices_4():
    pyramid = Hyperpyramid(4)

    assert len(pyramid.vertices) == 9


def test_get_facets():
    pyramid = Hyperpyramid(4)
    assert len(pyramid.facets) == 0
