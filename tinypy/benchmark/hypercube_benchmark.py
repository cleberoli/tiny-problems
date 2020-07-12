from typing import List

from tinypy.benchmark.base_benchmark import Benchmark
from tinypy.instances.hypercube_instance import HypercubeInstance


class HypercubeBenchmark(Benchmark):
    """Generates benchmarks for the Hypercube polytope.

    Extends the base Benchmark. This instance is not based on a graph and the
    points don't respect the euclidean constraints.
    """

    def __init__(self, **kwargs):
        """Initializes the benchmark for the Hypercube polytope.

        Args:
            **kwargs: A dictionary used to initialize the Hypercube instance.
        """
        self.instance = HypercubeInstance(**kwargs)
        self.euclidean = False
        Benchmark.__init__(self, HypercubeInstance(**kwargs), False)

    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            An empty list since this instance don't respect the triangle
            inequality constraints.
        """
        return []
