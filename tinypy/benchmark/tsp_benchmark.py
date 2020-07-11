from typing import List

from tinypy.benchmark.base_benchmark import Benchmark
from tinypy.graph.kn import Kn
from tinypy.instances.tsp_instance import TSPInstance


class TSPBenchmark(Benchmark):
    """Generates benchmarks for the Traveling Salesman polytope.

    Extends the base Benchmark. This instance is based on a graph and the points
    should respect the euclidean constraints.

    Attributes:
        instance: Reference to the problem instance class.
        euclidean: A boolean indicating whether the objective functions should
            respect euclidean constraints.
        benchmark_file: The path where the benchmark should be stored.
    """

    def __init__(self, **kwargs):
        """Initializes the benchmark for the Traveling Salesman polytope.

        Args:
            **kwargs: A dictionary used to initialize the Traveling Salesman
                instance.
        """
        Benchmark.__init__(self, TSPInstance(**kwargs), True)

    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            A list containing the triangles with each triangle being represented
            by a list of three vertices.
        """
        kn = Kn(self.instance.n)
        return kn.get_triangles()
