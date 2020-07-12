from typing import List

from tinypy.geometry.point import Point
from tinypy.graph.kn import Kn
from tinypy.instances.base_instance import Instance


class CutInstance(Instance):
    """Generates instance for the Cut problem.
    """

    def __init__(self, **kwargs):
        """Initializes the cut instance.

        Args:
            **kwargs: A dictionary containing the parameters.
        """
        if 'n' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['n'] <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        n = int(kwargs["n"])
        dimension = int(n * (n - 1) / 2)
        size = 2 ** (n - 1)

        Instance.__init__(self, f'CUT-n{n}', 'cut', dimension, size, n)

    def generate_solutions(self) -> List['Point']:
        """Generate the solution list.

        Returns:
            The solution list.
        """
        kn = Kn(self.n)
        cuts = kn.get_cuts()
        return list(cuts.values())
