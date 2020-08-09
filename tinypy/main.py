from tinypy.benchmark.hypercube_benchmark import HypercubeBenchmark

from tinypy.polytopes.base_polytope import Polytope
from tinypy.polytopes.cut_polytope import CutPolytope
from tinypy.polytopes.hyperpyramid_polytope import HyperpyramidPolytope
from tinypy.polytopes.hypercube_polytope import HypercubePolytope
from tinypy.polytopes.random_polytope import RandomPolytope
from tinypy.polytopes.tsp_polytope import TSPPolytope

from tinypy.trees.enumeration_tree import EnumerationTree
from tinypy.trees.tree_writer import TreeWriter


def run_all():
    for i in range(3, 8):
        HypercubePolytope(i)
        HyperpyramidPolytope(i)
        CutPolytope(i)
        TSPPolytope(i)

    RandomPolytope(3, 1)
    RandomPolytope(3, 4)
    RandomPolytope(6, 3)
    RandomPolytope(6, 8)
    RandomPolytope(10, 12)
    RandomPolytope(10, 16)
    RandomPolytope(15, 32)
    RandomPolytope(15, 60)
    RandomPolytope(21, 64)
    RandomPolytope(21, 360)


def generate_benchmark():
    benchmark = HypercubeBenchmark(n=3)
    benchmark.generate_benchmark()


def write_tree(polytope: Polytope):
    print(polytope)

    tree = EnumerationTree(polytope)
    tree.build_tree(recompute=True)
    print(f'HEIGHT: {tree.height}')

    tree_writer = TreeWriter(tree)
    tree_writer.write_tree()


def run_benchmark(polytope: Polytope):
    from tinypy.benchmark.benchmark_runner import BenchmarkRunner
    from tinypy.generated.trees.tsp.TSP_n5 import TSPTree

    runner = BenchmarkRunner(TSPTree(polytope))
    runner.run()


if __name__ == '__main__':
    polytope = TSPPolytope(5)
    write_tree(polytope)
    # run_benchmark(polytope)


