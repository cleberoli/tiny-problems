from tinypy.instances.hypercube_instance import HypercubeInstance
from tinypy.polytopes.base_polytope import Polytope


class HypercubePolytope(Polytope):
    """Extends the base polytope for hypercube instances.
    """

    def __init__(self, n: int):
        """Initializes the cub polytope with the Hypercube instance.

        Args:
            n: The number of dimensions.
        """
        Polytope.__init__(self, HypercubeInstance(n=n), 'hypercube', False)
