from tinypy.instances.hypercube_instance import HypercubeInstance
from tinypy.polytopes.base_polytope import Polytope


class HypercubePolytope(Polytope):

    def __init__(self, n: int):
        self.instance = HypercubeInstance(n=n)
        self.full_name = 'hypercube'

        Polytope.__init__(self)
