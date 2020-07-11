from typing import List

from tinypy.benchmark.base_benchmark import Benchmark
from tinypy.instances.hyperpyramid_instance import HyperpyramidInstance


class HyperpyramidBenchmark(Benchmark):
    """Generates benchmarks for the Hyperpyramid polytope.

    Extends the base Benchmark. This instance is not based on a graph and the
    points don't respect the euclidean constraints.

    Attributes:
        instance: Reference to the problem instance class.
        euclidean: A boolean indicating whether the objective functions should
            respect euclidean constraints.
        benchmark_file: The path where the benchmark should be stored.
    """

    def __init__(self, **kwargs):
        """Initializes the benchmark for the Hyperpyramid polytope.

        Args:
            **kwargs: A dictionary used to initialize the Hyperpyramid instance.
        """
        Benchmark.__init__(self, HyperpyramidInstance(**kwargs), False)

    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            An empty list since this instance don't respect the triangle
            inequality constraints.
        """
        return []
