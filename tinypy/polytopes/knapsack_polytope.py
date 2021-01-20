from tinypy.instances.knapsack_instance import KnapsackInstance
from tinypy.polytopes.base_polytope import Polytope


class KnapsackPolytope(Polytope):
    """Extends the base polytope for knapsack instances.
    """

    def __init__(self, n: int, origin: bool = False, save: bool = True):
        """Initializes the tsp polytope with the Traveling Salesman instance.

        Args:
            n: The number of nodes in the graph.
        """
        Polytope.__init__(self, KnapsackInstance(n=n, origin=origin, save=save), 'knapsack', save)
