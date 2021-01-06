from typing import List, Union

from tinypy.geometry.region import Region


class Node:

    hash: str
    region: List[int]
    solutions: List[int]
    hyperplanes: List[int]

    hyperplane: int
    height: int
    left: str
    right: str

    threshold: int
    explored: List[int]

    def __init__(self, region: Region, solutions: List[int], hyperplanes: List[int]):
        self.hash = repr(region)
        self.region = region.hyperplanes
        self.solutions = solutions
        self.hyperplanes = hyperplanes
        self.threshold = 0
        self.explored = []

    def set_leaf(self):
        self.set_node(0, -1)
        self.hyperplanes = []

    def set_node(self, height: int, threshold: int, hyperplane: int = None, left: str = None, right: str = None):
        self.height = height
        self.threshold = threshold
        self.hyperplane = hyperplane
        self.left = left
        self.right = right
