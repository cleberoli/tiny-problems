from abc import ABC, abstractmethod
from typing import Dict, List

from tinypy.geometry.point import Point


class Instance(ABC):

    solutions: List['Point']

    def __init__(self, **kwargs):
        self.solutions = self.generate_solutions(**kwargs)

    def get_solution_list(self) -> List['Point']:
        return self.solutions

    def get_solution_dict(self) -> Dict[int, 'Point']:
        return dict((key, self.solutions[key]) for key in range(len(self.solutions)))

    @abstractmethod
    def generate_solutions(self, **kwargs) -> List['Point']:
        pass
