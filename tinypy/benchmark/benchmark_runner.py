from math import isclose

from tinypy.generated.trees.generated_tree import GeneratedTree
from tinypy.geometry.point import Point
from tinypy.utils.file import get_full_path


class BenchmarkRunner:

    tree: GeneratedTree
    benchmark_file: str
    solutions_file: str

    def __init__(self, tree: GeneratedTree):
        self.tree = tree
        self.polytope = tree.polytope
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
            solutions = self.polytope.instance.get_solution_dict()
            heights = 0

            with open(self.solutions_file, 'w+') as output_file:
                for _ in range(instances):
                    line = input_file.readline().split(':')
                    solution = int(line[0])
                    point = Point(list(map(float, line[1].split())))
                    sol, node, height = self.tree.test(point)
                    same_solutions = solution == sol
                    equivalent_solutions = isclose(point * solutions[solution], point * solutions[sol], abs_tol=0.0001)
                    output_file.write(f'{same_solutions} {equivalent_solutions} {solution} {sol} {height} {node}\n')
                    heights = heights + height

                output_file.write(f'AVERAGE HEIGHT: {round(heights / instances, 4)}\n')
