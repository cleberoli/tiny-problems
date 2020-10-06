from tinypy.instances.tsp_instance import TSPInstance
from tinypy.polytopes.base_polytope import Polytope


class TSPPolytope(Polytope):
    """Extends the base polytope for traveling salesman instances.
    """

    def __init__(self, n: int):
        """Initializes the tsp polytope with the Traveling Salesman instance.

        Args:
            n: The number of nodes in the graph.
        """
        Polytope.__init__(self, TSPInstance(n=n), 'traveling salesman')
