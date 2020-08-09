from typing import List

from tinypy.geometry.point import Point
from tinypy.instances.base_instance import Instance
from tinypy.utils import combinatorics


class HyperpyramidInstance(Instance):
    """Generates instance for the hyperpyramid polytope.
    """

    def __init__(self, **kwargs):
        """Initializes the pyr instance.

        Args:
            **kwargs: A dictionary containing the parameters.
        """
        if 'n' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['n'] <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        n = int(kwargs["n"])
        dimension = n
        size = 2 ** (n - 1) + 1

        Instance.__init__(self, f'PYR-n{n}', 'pyr', dimension, size, n)

    def generate_solutions(self) -> List['Point']:
        """Generate the solution list.

        Returns:
            The solution list.
        """
        vertices = combinatorics.get_permutations([0, 2], self.n - 1)
        vertices = [Point(v + (0,)) for v in vertices]
        vertices.append(Point(tuple([1] * self.n)))
        return vertices

    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            An empty list since this instance don't respect the triangle
            inequality constraints.
        """
        return []
