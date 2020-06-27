from typing import List

from tinypy.geometry.point import Point
from tinypy.instances.base_instance import Instance
from tinypy.graph.kn import Kn


class TSPInstance(Instance):

    def __init__(self, **kwargs):
        if 'n' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['n'] <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        Instance.__init__(self, **kwargs)

    def generate_solutions(self, **kwargs) -> List['Point']:
        kn = Kn(kwargs['n'])
        cycles = kn.get_hamilton_cycles()
        return list(cycles.values())
        return []
