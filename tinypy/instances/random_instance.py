from typing import List

from tinypy.geometry.point import Point
from tinypy.instances.base_instance import Instance


class RandomInstance(Instance):

    def __init__(self, **kwargs):
        if 'd' not in kwargs or 'size' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['d'] <= 0 or kwargs['size'] <= 0:
            raise ValueError('The dimension and size must be greater than 0.')

        if kwargs['size'] > 2**kwargs['d']:
            raise ValueError('The size should be at most 2^d.')

        Instance.__init__(self, **kwargs)

    def generate_solutions(self, **kwargs) -> List['Point']:
        solutions = set()

        while len(solutions) < kwargs['size']:
            random_sols = [Point.random(kwargs['d']) for _ in range(kwargs['size'])]

            for sol in random_sols:
                solutions.add(sol)

        solutions = list(solutions)
        solutions.sort()

        return solutions[:kwargs['size']]
