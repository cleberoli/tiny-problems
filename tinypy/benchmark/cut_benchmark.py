from typing import List

from tinypy.benchmark.base_benchmark import Benchmark
from tinypy.graph.kn import Kn
from tinypy.instances.cut_instance import CutInstance


class CutBenchmark(Benchmark):
    """Generates benchmarks for the Cut polytope.

    Extends the base Benchmark. This instance is based on a graph and the points
    should respect the euclidean constraints.
    """

    def __init__(self, **kwargs):
        """Initializes the benchmark for the Cut polytope.

        Args:
            **kwargs: A dictionary used to initialize the Cut instance.
        """
        Benchmark.__init__(self, CutInstance(**kwargs), True)

    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            A list containing the triangles with each triangle being represented
            by a list of three vertices.
        """
        kn = Kn(self.instance.n)
        return kn.get_triangles()
