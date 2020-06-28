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

        n = int(kwargs["n"])
        self.name = f'TSP-n{n}'
        self.type = 'tsp'
        self.dimension = int(n * (n - 1) / 2)
        self.size = int(factorial(n - 1) / 2)

        Instance.__init__(self, **kwargs)

    def generate_solutions(self, **kwargs) -> List['Point']:
        kn = Kn(kwargs['n'])
        cycles = kn.get_hamilton_cycles()
        return list(cycles.values())
