from tinypy.instances.hyperpyramid_instance import HyperpyramidInstance
from tinypy.polytopes.base_polytope import Polytope


class HyperpyramidPolytope(Polytope):
    """Extends the base polytope for hyperpyramid instances.
    """

    def __init__(self, n: int):
        """Initializes the pyr polytope with the Hyperpyramid instance.

        Args:
            n: The number of dimensions.
        """
        Polytope.__init__(self, HyperpyramidInstance(n=n), 'hyperpyramid')
