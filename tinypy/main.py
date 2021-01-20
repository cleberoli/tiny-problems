# adding path to local module tinypy
import sys

sys.path.append('/home/coliveira/tiny-problems')


if __name__ == '__main__':
    from tinypy.polytopes.cut_polytope import CutPolytope
    from tinypy.polytopes.hypercube_polytope import HypercubePolytope
    from tinypy.polytopes.knapsack_polytope import KnapsackPolytope
    from tinypy.polytopes.tsp_polytope import TSPPolytope
    from tinypy.trees.iterative_tree import IterativeTree

    if len(sys.argv) < 3:
        raise ValueError('Not enough arguments.')

    p = sys.argv[1]
    n = int(sys.argv[2])
    origin = len(sys.argv) == 4 and sys.argv[3] == 'o'

    if p == 'cut':
        polytope = CutPolytope(n, origin)
    elif p == 'tsp':
        polytope = TSPPolytope(n, origin)
    elif p == 'knp':
        polytope = KnapsackPolytope(n, origin)
    else:
        polytope = HypercubePolytope(n)

    tree = IterativeTree(polytope)
    tree.build_tree()
