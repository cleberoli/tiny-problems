from math import isclose

from tinypy.generated.trees.generated_tree import GeneratedTree
from tinypy.geometry.point import Point
from tinypy.utils.file import get_full_path


class BenchmarkRunner:
    """Runs the benchmarks for the generated trees.

    Reads the benchmark files and runs the decision tree for each point.

    Attributes:
        tree: The decision tree generated.
        benchmark_file: The path where the benchmark should be stored.
        solution_file: The path where the solution should be stored.

    """

    tree: GeneratedTree
    benchmark_file: str
    solution_file: str

    def __init__(self, tree: GeneratedTree):
        """Initializes the runner.

        Args:
            tree: The decision tree corresponding to the benchmark.
        """
        self.tree = tree
        self.polytope = tree.polytope
        self.benchmark_file = get_full_path('files', 'benchmarks', self.polytope.instance.type, f'{self.polytope.instance.name}.tpbf')
        self.solution_file = get_full_path('files', 'benchmarks', self.polytope.instance.type, f'{self.polytope.instance.name}.sol')

    def run(self):
        """Runs the decision tree for the given benchmark file.

        The solutions file registers six elements for each benchmark point
        (whether the solutions are the same, whether they are equivalent,
        the benchmark solution, the solution found by the tree,
        the solution node, and the node's height).
        """
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
            pos, neg = 0, 0

            with open(self.solution_file, 'w+') as output_file:
                for _ in range(instances):
                    line = input_file.readline().split(':')
                    solution = int(line[0])
                    point = Point(list(map(float, line[1].split())))
                    sol, node, height, hyperplanes = self.tree.test(point)
                    same_solutions = solution == sol
                    equivalent_solutions = isclose(point * solutions[solution], point * solutions[sol], abs_tol=0.0001)
                    output_file.write(f'{same_solutions} {equivalent_solutions} {solution} {sol} {node} {height} {hyperplanes}\n')
                    heights = heights + height
                    if equivalent_solutions:
                        pos = pos + 1
                    else:
                        neg = neg + 1

                output_file.write(f'AVERAGE HEIGHT: {round(heights / instances, 4)}\n')
                output_file.write(f'POSITIVE: {pos} {round(pos / instances, 4)}\n')
                output_file.write(f'NEGATIVE: {neg} {round(neg / instances, 4)}\n')
                print(f'AVERAGE HEIGHT: {round(heights / instances, 4)}\n')
                print(f'POSITIVE: {pos} {round(pos / instances, 4)}\n')
                print(f'NEGATIVE: {neg} {round(neg / instances, 4)}\n')
