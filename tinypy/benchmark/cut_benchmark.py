from typing import List

from tinypy.benchmark.base_benchmark import Benchmark
from tinypy.graph.kn import Kn
from tinypy.instances.cut_instance import CutInstance


class CutBenchmark(Benchmark):

    def __init__(self, **kwargs):
        self.instance = CutInstance(**kwargs)
        self.euclidean = True
        Benchmark.__init__(self)

    def get_triangles(self) -> List[List[int]]:
        kn = Kn(self.instance.n)
        return kn.get_triangles()
