from abc import ABC, abstractmethod
from datetime import datetime
from os import path
from typing import Dict, List

from tinypy.geometry.point import Point
from tinypy.utils.file import create_directory, get_full_path


class Instance(ABC):
    """Base class that generates instance for different problems.

    Attributes:
        instance_file: The path where the instance should be stored.
        name: Instance name.
        type: Instance type.
        dimension: Instance dimension.
        size: Number of solutions.
        n: Main instance parameter.
        solutions: List of solution points.
    """

    instance_file: str
    name: str
    type: str
    dimension: int
    size: int
    n: int
    solutions: List['Point']

    def __init__(self, name: str, instance_type: str, dimension: int, size: int, n: int):
        """Initializes the instance.

        Args:
            name: Instance name.
            instance_type: Instance type.
            dimension: Instance dimension.
            size: Number of solutions.
            n: Main instance parameter.
        """
        self.name = name
        self.type = instance_type
        self.dimension = dimension
        self.size = size
        self.n = n
        self.instance_file = get_full_path('files', 'instances', self.type, f'{self.name}.tpif')
        create_directory(get_full_path('files', 'instances', self.type))

        if path.exists(self.instance_file):
            self.solutions = self.__read_instance_file()
        else:
            self.solutions = self.generate_solutions()
            self.__write_instance_file()

    def get_solution_list(self) -> List['Point']:
        """Returns the solutions as list of points.
        """
        return self.solutions

    def get_solution_dict(self) -> Dict[int, 'Point']:
        """Returns the solutions as dictionary.
        """
        return dict((key + 1, self.solutions[key]) for key in range(len(self.solutions)))

    def get_best_solution(self, point: Point) -> int:
        """Returns the solution the minimizes the given objective function.

        Args:
            point: A point representing the objective function.

        Returns:
            Index of the best solution.
        """
        min_value, min_solution = float('inf'), 0
        one = Point([1] * self.dimension)

        for index, solution in enumerate(self.solutions):
            x = (2 * solution) - one
            value = point * x

            if value < min_value:
                min_value, min_solution = value, index + 1

        return min_solution

    @abstractmethod
    def generate_solutions(self) -> List['Point']:  # pragma: no cover
        """Generate the solution list.

        Returns:
            The solution list.
        """
        pass

    def __read_instance_file(self) -> List['Point']:
        """Loads the instance from file.

        Returns:
            The solution list.
        """
        solutions = []

        with open(self.instance_file, 'r') as file:
            file.readline()             # name
            file.readline()             # type
            file.readline()             # generated
            file.readline()             # dimension
            file.readline()             # size
            file.readline()

            for i in range(self.size):
                coords = list(map(int, file.readline().split()))
                solutions.append(Point(coords))

        return solutions

    def __write_instance_file(self):
        """Writes the instance to a file.
        """
        now = datetime.now()

        with open(self.instance_file, 'w+') as file:
            file.write(f'NAME: {self.name}\n')
            file.write(f'TYPE: {self.type.upper()}\n')
            file.write(f'GENERATED: {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
            file.write(f'DIMENSION: {self.solutions[0].dim}\n')
            file.write(f'SIZE: {len(self.solutions)}\n\n')

            for solution in self.solutions:
                solution_str = ' '.join(map(str, solution))
                file.write(f'{solution_str}\n')
