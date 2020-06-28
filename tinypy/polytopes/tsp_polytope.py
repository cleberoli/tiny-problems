from tinypy.instances.tsp_instance import TSPInstance
from tinypy.polytopes.base_polytope import Polytope


class TSPPolytope(Polytope):

    def __init__(self, n: int):
        self.instance = TSPInstance(n=n)
        self.full_name = 'travelling salesman'

        Polytope.__init__(self)
