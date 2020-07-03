from typing import List

from tinypy.benchmark.base_benchmark import Benchmark
from tinypy.instances.hyperpyramid_instance import HyperpyramidInstance


class HyperpyramidBenchmark(Benchmark):

    def __init__(self, **kwargs):
        self.instance = HyperpyramidInstance(**kwargs)
        self.euclidean = False
        Benchmark.__init__(self)

    def get_triangles(self) -> List[List[int]]:
        return []
