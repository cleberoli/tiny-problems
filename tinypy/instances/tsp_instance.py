from math import factorial
from typing import List

from tinypy.geometry.point import Point
from tinypy.graph.kn import Kn
from tinypy.instances.base_instance import Instance


class TSPInstance(Instance):
    """Generates instance for the Traveling Salesman problem.
    """

    def __init__(self, **kwargs):
        """Initializes the tsp instance.

        Args:
            **kwargs: A dictionary containing the parameters.
        """
        if 'n' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['n'] <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        n = int(kwargs["n"])
        dimension = int(n * (n - 1) / 2)
        size = int(factorial(n - 1) / 2)

        Instance.__init__(self, f'TSP-n{n}', 'tsp', dimension, size, n)

    def generate_solutions(self) -> List['Point']:
        """Generate the solution list.

        Returns:
            The solution list.
        """
        kn = Kn(self.n)
        cycles = kn.get_hamilton_cycles()
        return list(cycles.values())

    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            A list containing the triangles with each triangle being represented
            by a list of three vertices.
        """
        kn = Kn(self.n)
        return kn.get_triangles()
