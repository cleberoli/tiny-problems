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

        self.n = int(kwargs["n"])
        self.dimension = self.n
        self.size = 2 ** (self.n - 1) + 1
        self.name = f'PYR-n{self.n}'
        self.type = 'pyr'

        Instance.__init__(self)

    def generate_solutions(self) -> List['Point']:
        vertices = combinatorics.get_permutations([0, 2], self.n - 1)
        vertices = [Point(v + (0,)) for v in vertices]
        vertices.append(Point(tuple([1] * self.n)))
        return vertices
