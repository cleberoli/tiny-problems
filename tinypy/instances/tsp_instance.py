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

        kwargs['type'] = 'tsp'
        kwargs['name'] = f'TSP-n{kwargs["n"]}'

        Instance.__init__(self, **kwargs)

    def generate_solutions(self, **kwargs) -> List['Point']:
        kn = Kn(kwargs['n'])
        cycles = kn.get_hamilton_cycles()
        return list(cycles.values())
