from tinypy.instances.random_instance import RandomInstance
from tinypy.polytopes.base_polytope import Polytope


class RandomPolytope(Polytope):
    """Extends the base polytope for random instances.
    """

    def __init__(self, d: int, m: int):
        """Initializes the rnd polytope with the Random instance.

        Args:
            d: The number of dimensions.
            m: The number of solutions.
        """
        Polytope.__init__(self, RandomInstance(d=d, m=m), 'random')
