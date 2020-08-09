from typing import List

from tinypy.polytopes.base_polytope import Polytope
from tinypy.trees.base_tree import Tree


class EnumerationTree(Tree):
    """Implementation of base tree for the enumeration algorithm.

    The function to select the next hyperplane mimics the enumeration algorithm
    but uses the information of intersections to discard some solutions.
    """

    def __init__(self, polytope: Polytope, bfs=False):
        """Initializes the enumeration tree.

        Args:
            polytope: The given polytope.
        """
        Tree.__init__(self, polytope, bfs)

    def select_hyperplane(self, solutions: List[int]) -> int:
        """Selects the next hyperplane given the possible solutions.

        Selects the bisector of the first two solutions.

        Args:
            solutions: The list of possible solution indices.

        Returns:
            Index of the next hyperplane.
        """
        sol_i, sol_j = solutions[0], solutions[1]
        hyperplane = self.polytope.get_bisector(sol_i, sol_j)

        return hyperplane
