import random

from functools import total_ordering
from math import sqrt
from typing import List, Union


@total_ordering
class Point:

    coords: tuple
    dim: int

    def __init__(self, *args):
        if type(args[0]) is list or type(args[0]) is tuple:
            args = tuple(args[0])

        if all(isinstance(x, int) for x in args) or all(isinstance(x, float) for x in args):
            self.coords = args
            self.dim = len(self.coords)
        else:
            raise ValueError('Invalid parameter.')

    @classmethod
    def origin(cls, dim: int) -> 'Point':
        """A point of all zeros of the same dimension as the current point"""
        return cls([0] * dim)

    @classmethod
    def random(cls, dim: int, a: int = 0, b: int = 1, decimals: int = 0, norm: int = None) -> 'Point':
        args = [random.randint(a, b) for _ in range(dim)] if decimals == 0 else [round(random.uniform(a, b), decimals) for _ in range(dim)]
        point = cls(args)

        if norm is not None:
            unitary_point = point * (norm / point.norm)
            point = cls([round(i, max(decimals, 4)) for i in unitary_point.coords])

        return point

    @classmethod
    def random_triangle(cls, dim: int, triangles: List[List[int]], a: int = 0, b: int = 1, decimals: int = 4, norm: int = 1) -> 'Point':
        point = cls.random(dim, a, b, decimals)

        while not point.respects_triangle_inequality(triangles):
            point = cls.random(dim, a, b, decimals)

        unitary_point = point * (norm / point.norm)
        unitary_point = cls([round(i, max(decimals, 4)) for i in unitary_point.coords])

        return unitary_point

    @property
    def homogeneous_coords(self) -> tuple:
        return self.coords + (1, )

    @property
    def norm(self) -> float:
        return self.distance(self.origin(self.dim))

    def distance(self, other: 'Point') -> float:
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return sqrt(sum(list(map(lambda x: x * x, (self - other).coords))))

    def add_coord(self, coord: Union[int, float]):
        if not isinstance(coord, type(self.coords[0])):
            raise ValueError('The types are not compatible.')

        self.coords = self.coords + (coord, )
        self.dim = self.dim + 1

    def respects_triangle_inequality(self, triangles: List[List[int]]):
        for triangle in triangles:
            if self.coords[triangle[0]] + self.coords[triangle[1]] <= self.coords[triangle[2]]:
                return False
            if self.coords[triangle[0]] + self.coords[triangle[2]] <= self.coords[triangle[1]]:
                return False
            if self.coords[triangle[1]] + self.coords[triangle[2]] <= self.coords[triangle[0]]:
                return False

        return True

    def __add__(self, other: 'Point') -> 'Point':
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return Point(list(map(lambda x, y: x + y, self.coords, other.coords)))

    def __sub__(self, other: 'Point') -> 'Point':
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return Point(list(map(lambda x, y: x - y, self.coords, other.coords)))

    def __rmul__(self, other: Union['Point', int, float]) -> Union['Point', int, float]:
        # dot product
        if isinstance(other, Point):
            if self.dim != other.dim:
                raise ValueError('The dimensions are not compatible.')

            return sum(list(map(lambda x, y: x * y, self.coords, other.coords)))

        # multiplication by a scalar
        elif isinstance(other, int) or isinstance(other, float):
            return Point(list(map(lambda x: x * other, self.coords)))

        else:
            raise ValueError('Invalid operation.')

    __mul__ = __rmul__

    def __neg__(self):
        return -1 * self

    def __getitem__(self, item: int):
        return self.coords[item]

    def __hash__(self):
        return hash(repr(self))

    def __lt__(self, other: 'Point'):
        return self.coords < other.coords

    def __gt__(self, other: 'Point'):
        return not (self <= other)

    def __eq__(self, other: 'Point'):
        return self.coords == other.coords

    def __ne__(self, other: 'Point'):
        return not (self == other)

    def __str__(self):
        return str(self.coords)

    def __repr__(self):
        return str(self.coords)
