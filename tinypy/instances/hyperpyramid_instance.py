from typing import List

from tinypy.geometry.point import Point
from tinypy.instances.base_instance import Instance
from tinypy.utils import combinatorics


class HyperpyramidInstance(Instance):

    def __init__(self, **kwargs):
        if 'n' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['n'] <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        Instance.__init__(self, **kwargs)

    def generate_solutions(self, **kwargs) -> List['Point']:
        vertices = combinatorics.get_permutations([0, 2], kwargs['n'] - 1)
        vertices = [Point(v + (0,)) for v in vertices]
        vertices.append(Point(tuple([1] * kwargs['n'])))
        return vertices
