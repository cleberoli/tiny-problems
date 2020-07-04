from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple

from tinypy.geometry.point import Point
from tinypy.instances.base_instance import Instance
from tinypy.utils.file import create_folder, get_full_path


class Benchmark(ABC):

    instance: Instance
    euclidean: bool
    benchmark_file: str

    def __init__(self):
        create_folder(get_full_path('files', 'benchmarks', self.instance.type))

    def generate_benchmark(self, size: int = 10000):
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
    def get_triangles(self):
        pass
