from typing import List

from tinypy.geometry.point import Point
from tinypy.instances.base_instance import Instance
from tinypy.utils.combinatorics import get_distinct_partitions


class KnapsackInstance(Instance):
    """Generates instance for the Knapsack problem.
    """

    def __init__(self, **kwargs):
        """Initializes the cut instance.

        Args:
            **kwargs: A dictionary containing the parameters.
        """
        if 'n' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['n'] <= 1:
            raise ValueError('The dimensions must be greater than 1.')

        n = int(kwargs['n'])
        origin = bool(kwargs['origin']) if 'origin' in kwargs else True
        save = bool(kwargs['save']) if 'save' in kwargs else True
        dimension = n
        size = self.__compute_size(n)

        if origin:
            size = size + 1

        Instance.__init__(self, f'KNP-n{n}', 'knp', dimension, size, n, origin, save)

    def generate_solutions(self) -> List[Point]:
        solutions = [Point.origin(self.dimension)] if self.origin else []

        for i in range(1, self.n + 1):
            partitions = get_distinct_partitions(i)

            for p in partitions:
                coords = [0] * self.dimension

                for index in p:
                    coords[index - 1] = 1

                solutions.append(Point(coords))

        return solutions

    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            A list containing the triangles with each triangle being represented
            by a list of three vertices.
        """
        return []

    @staticmethod
    def __compute_size(n: int):
        partial_sum = 0

        for i in range(1, n + 1):
            partial_sum += len(get_distinct_partitions(i))

        return partial_sum
