from bisect import insort
from typing import List


class Region:

    hyperplanes: List[int]

    def __init__(self, hyperplanes: List[int] = None):
        self.hyperplanes = hyperplanes if hyperplanes is not None else []
        self.hyperplanes.sort()

    def add_hyperplane(self, hyperplane: int):
        insort(self.hyperplanes, hyperplane)

    def union(self, region: 'Region'):
        hyperplane_set = set(self.hyperplanes).union(set(region.hyperplanes))
        return Region(sorted(list(hyperplane_set)))

    def __str__(self):
        return str(self.hyperplanes)

    def __repr__(self):
        return repr(self.hyperplanes)
