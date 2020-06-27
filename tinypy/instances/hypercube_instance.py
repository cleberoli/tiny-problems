from typing import List

from tinypy.geometry.point import Point
from tinypy.instances.base_instance import Instance
from tinypy.utils import combinatorics


class HypercubeInstance(Instance):

    def __init__(self, **kwargs):
        if 'n' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['n'] <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        kwargs['type'] = 'cub'
        kwargs['name'] = f'CUB-n{kwargs["n"]}'

        Instance.__init__(self, **kwargs)

    def generate_solutions(self, **kwargs) -> List['Point']:
        vertices = combinatorics.get_permutations([0, 1], kwargs['n'])
        vertices = [Point(v) for v in vertices]
        return vertices

