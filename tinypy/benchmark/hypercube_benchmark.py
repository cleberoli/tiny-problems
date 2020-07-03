from typing import List

from tinypy.benchmark.base_benchmark import Benchmark
from tinypy.instances.hypercube_instance import HypercubeInstance


class HypercubeBenchmark(Benchmark):

    def __init__(self, **kwargs):
        self.instance = HypercubeInstance(**kwargs)
        self.euclidean = False
        Benchmark.__init__(self)

    def get_triangles(self) -> List[List[int]]:
        return []
