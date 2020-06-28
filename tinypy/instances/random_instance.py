from typing import List

from tinypy.geometry.point import Point
from tinypy.instances.base_instance import Instance


class RandomInstance(Instance):

    def __init__(self, **kwargs):
        if 'd' not in kwargs or 'm' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['d'] <= 0 or kwargs['m'] <= 0:
            raise ValueError('The dimension and size must be greater than 0.')

        if kwargs['m'] > 2**kwargs['d']:
            raise ValueError('The size should be at most 2^d.')

        self.n = int(kwargs["m"])
        self.dimension = int(kwargs["d"])
        self.size = int(kwargs["m"])
        self.name = f'RND-d{self.dimension}-m{self.size}'
        self.type = 'rnd'

        Instance.__init__(self)

    def generate_solutions(self) -> List['Point']:
        solutions = set()

        while len(solutions) < self.size:
            random_sols = [Point.random(self.dimension) for _ in range(self.size)]

            for sol in random_sols:
                solutions.add(sol)

        solutions = list(solutions)
        solutions.sort()

        return solutions[:self.size]
