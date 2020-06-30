from abc import ABC, abstractmethod
from datetime import datetime
from os import path
from typing import Dict, List

from tinypy.geometry.point import Point
from tinypy.utils.file import get_full_path


class Instance(ABC):

    instance_file: str
    name: str
    type: str
    dimension: int
    size: int
    n: int
    solutions: List['Point']

    def __init__(self):
        self.instance_file = get_full_path('files', 'instances', self.type, f'{self.name}.tpif')

        if path.exists(self.instance_file):
            self.solutions = self.__read_instance_file()
        else:
            self.solutions = self.generate_solutions()
            self.__write_instance_file()

    def get_solution_list(self) -> List['Point']:
        return self.solutions

    def get_solution_dict(self) -> Dict[int, 'Point']:
        return dict((key + 1, self.solutions[key]) for key in range(len(self.solutions)))

    @abstractmethod
    def generate_solutions(self) -> List['Point']:  # pragma: no cover
        pass

    def __read_instance_file(self):
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
