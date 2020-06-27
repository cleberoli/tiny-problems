from abc import ABC, abstractmethod
from datetime import datetime
from os import path
from typing import Dict, List

from tinypy.geometry.point import Point


class Instance(ABC):

    instance_file: str
    solutions: List['Point']

    def __init__(self, **kwargs):
        self.instance_file = f'../instances/{kwargs["type"]}/{kwargs["name"]}.tpi'

        if path.exists(self.instance_file):
            self.solutions = self.read_instance_file()
        else:
            self.solutions = self.generate_solutions(**kwargs)
            self.write_instance_file(**kwargs)

    def get_solution_list(self) -> List['Point']:
        return self.solutions

    def get_solution_dict(self) -> Dict[int, 'Point']:
        return dict((key, self.solutions[key]) for key in range(len(self.solutions)))

    def read_instance_file(self):
        solutions = []

        with open(self.instance_file, 'r') as file:
            file.readline()             # name
            file.readline()             # type
            file.readline()             # generated
            file.readline()             # dimension
            line = file.readline()      # size
            size = int(line.split(':')[1].strip())
            file.readline()

            for i in range(size):
                coords = list(map(int, file.readline().split()))
                solutions.append(Point(coords))

        return solutions

    def write_instance_file(self, **kwargs):
        now = datetime.now()

        with open(self.instance_file, 'w') as file:
            file.write(f'NAME: {kwargs["name"]}\n')
            file.write(f'TYPE: {kwargs["type"].upper()}\n')
            file.write(f'GENERATED: {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
            file.write(f'DIMENSION: {self.solutions[0].dim}\n')
            file.write(f'SIZE: {len(self.solutions)}\n\n')

            for solution in self.solutions:
                solution_str = ' '.join(map(str, solution))
                file.write(f'{solution_str}\n')

    @abstractmethod
    def generate_solutions(self, **kwargs) -> List['Point']:
        pass
