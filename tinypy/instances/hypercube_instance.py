from typing import List

from tinypy.geometry.point import Point
from tinypy.instances.base_instance import Instance
from tinypy.utils import combinatorics


class HypercubeInstance(Instance):
    """Generates instance for the hypercube polytope.
    """

    def __init__(self, **kwargs):
        """Initializes the cub instance.

        Args:
            **kwargs: A dictionary containing the parameters.
        """
        if 'n' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['n'] <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        n = int(kwargs["n"])
        dimension = n
        size = 2 ** n

        Instance.__init__(self, f'CUB-n{n}', 'cub', dimension, size, n, False, False)

    def generate_solutions(self) -> List[Point]:
        """Generate the solution list.

        Returns:
            The solution list.
        """
        vertices = combinatorics.get_permutations([0, 1], self.n)
        vertices = [Point(v) for v in vertices]
        return vertices

    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            An empty list since this instance don't respect the triangle
            inequality constraints.
        """
        return []
