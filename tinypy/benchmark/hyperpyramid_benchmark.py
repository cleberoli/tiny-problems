from tinypy.benchmark.base_benchmark import Benchmark
from tinypy.instances.hyperpyramid_instance import HyperpyramidInstance


class HyperpyramidBenchmark(Benchmark):
    """Generates benchmarks for the Hyperpyramid polytope.

    Extends the base Benchmark. This instance is not based on a graph and the
    points don't respect the euclidean constraints.
    """

    def __init__(self, **kwargs):
        """Initializes the benchmark for the Hyperpyramid polytope.

        Args:
            **kwargs: A dictionary used to initialize the Hyperpyramid instance.
        """
        Benchmark.__init__(self, HyperpyramidInstance(**kwargs), False)
