from tinypy.instances.cut_instance import CutInstance
from tinypy.polytopes.base_polytope import Polytope


class CutPolytope(Polytope):
    """Extends the base polytope for cut instances.
    """

    def __init__(self, n: int, origin: bool = False, save: bool = True):
        """Initializes the cut polytope with the Cut instance.

        Args:
            n: The number of nodes in the graph.
        """
        Polytope.__init__(self, CutInstance(n=n, origin=origin, save=save), 'cut', save)
