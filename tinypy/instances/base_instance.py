from abc import ABC, abstractmethod
from typing import Dict, List

from tinypy.geometry.point import Point
from tinypy.models.instance import Instance as DBInstance


class Instance(ABC):
    """Base class that generates instance for different problems.

    Attributes:
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
    solutions: List[Point]

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

        instance = DBInstance(self.name, self.type, self.dimension, self.size)
        doc = instance.get_doc()

        if doc is not None:
            self.solutions = list(instance.solutions.values())
        else:
            self.solutions = self.generate_solutions()
            instance.solutions = self.get_solution_dict()
            instance.add_doc()

    def get_solution_list(self) -> List[Point]:
        """Returns the solutions as list of points.
        """
        return self.solutions

    def get_solution_dict(self) -> Dict[int, Point]:
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
    def generate_solutions(self) -> List[Point]:  # pragma: no cover
        """Generate the solution list.

        Returns:
            The solution list.
        """
        pass

    @abstractmethod
    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            A list containing the triangles with each triangle being represented
            by a list of three vertices.
        """
        pass
