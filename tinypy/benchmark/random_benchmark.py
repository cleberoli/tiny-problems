from typing import List

from tinypy.benchmark.base_benchmark import Benchmark
from tinypy.instances.random_instance import RandomInstance


class RandomBenchmark(Benchmark):

    def __init__(self, **kwargs):
        self.instance = RandomInstance(**kwargs)
        self.euclidean = False
        Benchmark.__init__(self)

    def get_triangles(self) -> List[List[int]]:
        return []
