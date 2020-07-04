from tinypy.generated.trees.tsp.TSP_n5 import TSPTree
from tinypy.geometry.point import Point
from tinypy.polytopes.tsp_polytope import TSPPolytope
from tinypy.utils.file import get_full_path


class BenchmarkRunner:

    polytope: TSPPolytope
    tree: TSPTree
    benchmark_file: str
    solutions_file: str

    def __init__(self):
        self.polytope = TSPPolytope(5)
        self.tree = TSPTree(self.polytope)
        self.benchmark_file = get_full_path('files', 'benchmarks', self.polytope.instance.type, f'{self.polytope.instance.name}.tpbf')
        self.solutions_file = get_full_path('files', 'benchmarks', self.polytope.instance.type, f'{self.polytope.instance.name}.sol')

    def run(self):
        with open(self.benchmark_file, 'r') as input_file:
            input_file.readline()       # name
            input_file.readline()       # type
            input_file.readline()       # generated
            input_file.readline()       # dimension
            input_file.readline()       # size
            instances = int(input_file.readline().split()[1])
            input_file.readline()

            with open(self.solutions_file, 'w+') as output_file:
                for _ in range(instances):
                    line = input_file.readline().split(':')
                    solution = int(line[0])
                    point = Point(list(map(float, line[1].split())))
                    sol, node, height = self.tree.test(point)
                    output_file.write(f'{solution} {sol} {height} {node}\n')
