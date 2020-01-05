import pytest

from tinypy.geometry import Point
from tinypy.polytopes import Hypercube


def test_invalid_hypercube():
    with pytest.raises(ValueError):
        Hypercube(2)


def test_get_vertices_3():
    cube = Hypercube(3)
    expected_vertices = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]

    assert len(cube.vertices) == 8
    assert all([a == Point(b) for a, b in zip(cube.vertices, expected_vertices)])


def test_get_vertices_4():
    cube = Hypercube(4)

    assert len(cube.vertices) == 16


def test_get_facets():
    cube = Hypercube(4)
    assert len(cube.facets) == 0
