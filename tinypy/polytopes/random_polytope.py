from tinypy.instances.random_instance import RandomInstance
from tinypy.polytopes.base_polytope import Polytope


class RandomPolytope(Polytope):

    def __init__(self, d: int, m: int):
        self.instance = RandomInstance(d=d, m=m)
        self.full_name = 'random'

        Polytope.__init__(self)
