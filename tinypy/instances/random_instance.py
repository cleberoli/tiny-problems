from typing import List

from tinypy.geometry.point import Point
from tinypy.instances.base_instance import Instance


class RandomInstance(Instance):
    """Generates instance for the random polytope.
    """

    def __init__(self, **kwargs):
        """Initializes the rnd instance.

        Args:
            **kwargs: A dictionary containing the parameters.
        """
        if 'd' not in kwargs or 'm' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['d'] <= 0 or kwargs['m'] <= 0:
            raise ValueError('The dimension and size must be greater than 0.')

        if kwargs['m'] > 2**kwargs['d']:
            raise ValueError('The size should be at most 2^d.')

        n = int(kwargs["m"])
        dimension = int(kwargs["d"])
        size = int(kwargs["m"])

        Instance.__init__(self, f'RND-d{dimension}-m{size}', 'rnd', dimension, size, n)

    def generate_solutions(self) -> List['Point']:
        """Generate the solution list.

        Returns:
            The solution list.
        """
        solutions = set()

        while len(solutions) < self.size:
            random_sols = [Point.random(self.dimension) for _ in range(self.size)]

            for sol in random_sols:
                solutions.add(sol)

        solutions = list(solutions)
        solutions.sort()

        return solutions[:self.size]
