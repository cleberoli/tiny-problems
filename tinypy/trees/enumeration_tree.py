from typing import List

from tinypy.polytopes.base_polytope import Polytope
from tinypy.trees.tree import Tree


class EnumerationTree(Tree):

    def __init__(self, polytope: Polytope):
        Tree.__init__(self, polytope)

    def select_hyperplane(self, solutions: List[int]) -> int:
        sol_i, sol_j = solutions[0], solutions[1]
        hyperplane = self.polytope.get_bisector(sol_i, sol_j)

        return hyperplane
