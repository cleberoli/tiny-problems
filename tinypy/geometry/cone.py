from typing import List

from tinypy.geometry import Hyperplane, Point


class Cone:

    def __init__(self, tag: int, vertex: 'Point', hyperplanes: List['Hyperplane']):
        self.tag = tag
        self.vertex = vertex
        self.hyperplanes = hyperplanes
        self.hyperplanes.sort()
