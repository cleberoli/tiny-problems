from abc import ABC
from typing import Dict

from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.point import Point
from tinypy.polytopes.base_polytope import Polytope


class GeneratedTree(ABC):

    polytope: Polytope
    hyperplanes: Dict[int, Hyperplane]

    def __init__(self, polytope: Polytope):
        self.polytope = polytope
        self.hyperplanes = polytope.H
        self.hyperplanes.update(polytope.extended_H)

    def test(self, point: Point):
        pass
