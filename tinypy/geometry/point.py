import random

from functools import total_ordering
from math import sqrt
from typing import Union


@total_ordering
class Point:

    __coords: tuple
    __dim: int

    def __init__(self, *args):
        if type(args[0]) is list or type(args[0]) is tuple:
            args = tuple(args[0])

        if all(isinstance(x, int) for x in args) or all(isinstance(x, float) for x in args):
            self.__coords = args
            self.__dim = len(self.__coords)
        else:
            raise ValueError('Invalid parameter.')

    @classmethod
    def random(cls, dim: int, a: int = 0, b: int = 1) -> 'Point':
        args = [random.randint(a, b) for _ in range(dim)]
        return cls(args)

    @classmethod
    def origin(cls, dim: int) -> 'Point':
        """A point of all zeros of the same dimension as the current point"""
        return cls([0] * dim)

    @property
    def coords(self) -> tuple:
        return self.__coords

    @property
    def dim(self) -> int:
        return self.__dim

    @property
    def norm(self) -> float:
        return self.distance(self.origin(self.__dim))

    def distance(self, other: 'Point') -> float:
        if self.__dim != other.__dim:
            raise ValueError('The dimensions are not compatible.')

        return sqrt(sum(list(map(lambda x: x * x, (self - other).__coords))))

    def __add__(self, other: 'Point'):
        if self.__dim != other.__dim:
            raise ValueError('The dimensions are not compatible.')

        return Point(list(map(lambda x, y: x + y, self.__coords, other.__coords)))

    def __sub__(self, other: 'Point'):
        if self.__dim != other.__dim:
            raise ValueError('The dimensions are not compatible.')

        return Point(list(map(lambda x, y: x - y, self.__coords, other.__coords)))

    def __rmul__(self, other: Union['Point', int, float]):
        # dot product
        if isinstance(other, Point):
            if self.__dim != other.__dim:
                raise ValueError('The dimensions are not compatible.')

            return sum(list(map(lambda x, y: x * y, self.__coords, other.__coords)))
        # multiplication by a scalar
        elif isinstance(other, int) or isinstance(other, float):
            return Point(list(map(lambda x: x * other, self.__coords)))

    __mul__ = __rmul__

    def __neg__(self):
        return Point([-c for c in self.__coords])

    def __getitem__(self, item: int):
        return self.__coords[item]

    def __lt__(self, other: 'Point'):
        return self.__coords < other.__coords

    def __gt__(self, other: 'Point'):
        return self.__coords > other.__coords

    def __eq__(self, other: 'Point'):
        return self.__coords == other.__coords

    def __ne__(self, other: 'Point'):
        return not (self == other)

    def __repr__(self):
        return str(self.__coords)

    def __hash__(self):
        return hash(repr(self))


