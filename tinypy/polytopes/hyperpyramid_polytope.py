from tinypy.instances.hyperpyramid_instance import HyperpyramidInstance
from tinypy.polytopes.base_polytope import Polytope


class HyperpyramidPolytope(Polytope):

    def __init__(self, n: int):
        self.instance = HyperpyramidInstance(n=n)
        self.full_name = 'hyperpyramid'

        Polytope.__init__(self)
