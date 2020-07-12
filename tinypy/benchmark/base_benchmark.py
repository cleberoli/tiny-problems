from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple

from tinypy.geometry.point import Point
from tinypy.instances.base_instance import Instance
from tinypy.utils.file import create_directory, get_full_path


class Benchmark(ABC):
    """Base class that generates possible objective functions.

    Based on the dimension and size of instance types this class generates files
    containing possible objective functions that makes sense for the specified
    instance.

    There is also a possibility to consider whether the generate vectors should
    respect euclidean constraints (i.e. positivity and triangle inequality),
    in which case the implemented subclass should define which triangles to
    consider.

    Attributes:
        instance: Reference to the problem instance class.
        euclidean: A boolean indicating whether the objective functions should
            respect euclidean constraints.
        benchmark_file: The path where the benchmark should be stored.
    """

    instance: Instance
    euclidean: bool
    benchmark_file: str

    def __init__(self, instance: Instance, euclidean: bool):
        """Initializes the benchmark with the given instance.

        Args:
            instance: Reference to the problem instance class.
            euclidean: A boolean indicating whether the objective functions
                should respect euclidean constraints.
        """
        self.instance = instance
        self.euclidean = euclidean
        create_directory(get_full_path('files', 'benchmarks', self.instance.type))

    def generate_benchmark(self, size: int = 10000):
        """Generate the benchmark file with the required number of points.

        The file generated contains unique points where for each solutions there
        are 'size' points that attain their best for the given solution.

        Args:
            size: The number of points to be generated for each solution.
        """
        self.benchmark_file = get_full_path('files', 'benchmarks', self.instance.type, f'{self.instance.name}.tpbf')
        points_solutions = []
        solutions = set()
        frequencies = dict((key + 1, 0) for key in range(self.instance.size))

        while len(solutions) < size * self.instance.size:
            if self.euclidean:
                point = Point.random_triangle(self.instance.dimension, self.get_triangles())
            else:
                point = Point.random(self.instance.dimension, a=-1, b=1, decimals=4, norm=1)

            solution = self.instance.get_best_solution(point)

            if point not in solutions:
                if frequencies[solution] < size:
                    solutions.add(point)
                    frequencies[solution] = frequencies[solution] + 1
                    points_solutions.append((point, solution))

        self.__write_instance_file(points_solutions)

    def __write_instance_file(self, points_solutions: List[Tuple[Point, int]]):
        """Writes the generations points along with their solutions.

        Args:
            points_solutions: A list containing the points with their respective
                solutions.
        """
        now = datetime.now()

        with open(self.benchmark_file, 'w+') as file:
            file.write(f'NAME: {self.instance.name}\n')
            file.write(f'TYPE: {self.instance.type.upper()}\n')
            file.write(f'GENERATED: {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
            file.write(f'DIMENSION: {self.instance.dimension}\n')
            file.write(f'SIZE: {self.instance.size}\n')
            file.write(f'INSTANCES: {len(points_solutions)}\n\n')

            for point in points_solutions:
                solution_str = ' '.join(map(str, point[0]))
                file.write(f'{point[1]}: {solution_str}\n')

    @abstractmethod
    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            A list containing the triangles with each triangle being represented
            by a list of three vertices.
        """
        pass
