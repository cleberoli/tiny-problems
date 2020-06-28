from tinypy.instances.cut_instance import CutInstance
from tinypy.polytopes.base_polytope import Polytope


class CutPolytope(Polytope):

    def __init__(self, n: int):
        self.instance = CutInstance(n=n)
        self.full_name = 'cut'

        Polytope.__init__(self)
