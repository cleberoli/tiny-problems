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

        self.n = int(kwargs["n"])
        self.dimension = self.n
        self.size = 2 ** self.n
        self.name = f'CUB-n{self.n}'
        self.type = 'cub'

        Instance.__init__(self)

    def generate_solutions(self) -> List['Point']:
        vertices = combinatorics.get_permutations([0, 1], self.n)
        vertices = [Point(v) for v in vertices]
        return vertices

