from tinypy.benchmark.base_benchmark import Benchmark
from tinypy.instances.tsp_instance import TSPInstance


class TSPBenchmark(Benchmark):
    """Generates benchmarks for the Traveling Salesman polytope.

    Extends the base Benchmark. This instance is based on a graph and the points
    should respect the euclidean constraints.
    """

    def __init__(self, **kwargs):
        """Initializes the benchmark for the Traveling Salesman polytope.

        Args:
            **kwargs: A dictionary used to initialize the Traveling Salesman
                instance.
        """
        Benchmark.__init__(self, TSPInstance(**kwargs), True)
