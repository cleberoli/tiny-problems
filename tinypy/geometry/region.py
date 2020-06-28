from typing import Dict

from tinypy.geometry.hyperplane import Hyperplane


class Region:

    def __init__(self, dim: int, hyperplanes: Dict[int, 'Hyperplane'] = None):
        self.hyperplanes = hyperplanes if hyperplanes is not None else dict()
        self.dim = dim

    def add_hyperplane(self, key: int, hyperplane: 'Hyperplane'):
        self.hyperplanes[key] = hyperplane

    def union(self, region: 'Region'):
        current_dict = self.hyperplanes.copy()
        region_dict = region.hyperplanes.copy()
        return Region(self.dim, {**current_dict, **region_dict})

    def __str__(self):
        region = dict((key, str(self.hyperplanes[key])) for key in self.hyperplanes.keys())
        return str(region).replace("'", "").replace('"', '')

    def __repr__(self):
        return repr(self.hyperplanes)
