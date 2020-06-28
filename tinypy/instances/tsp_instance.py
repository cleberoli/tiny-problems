from math import factorial
from typing import List

from tinypy.geometry.point import Point
from tinypy.graph.kn import Kn
from tinypy.instances.base_instance import Instance


class TSPInstance(Instance):

    def __init__(self, **kwargs):
        if 'n' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['n'] <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        self.n = int(kwargs["n"])
        self.dimension = int(self.n * (self.n - 1) / 2)
        self.size = int(factorial(self.n - 1) / 2)
        self.name = f'TSP-n{self.n}'
        self.type = 'tsp'

        Instance.__init__(self)

    def generate_solutions(self) -> List['Point']:
        kn = Kn(self.n)
        cycles = kn.get_hamilton_cycles()
        return list(cycles.values())
