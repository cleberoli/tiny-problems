from tinypy.polytopes.base_polytope import Polytope
from tinypy.polytopes.cut_polytope import CutPolytope
from tinypy.polytopes.hypercube_polytope import HypercubePolytope
from tinypy.polytopes.tsp_polytope import TSPPolytope

from tinypy.trees.iterative_tree import IterativeTree

if __name__ == '__main__':
    polytope = CutPolytope(3)
    # polytope = TSPPolytope(5)

    tree = IterativeTree(polytope)
    tree.build_tree()

