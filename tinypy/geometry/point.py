from functools import total_ordering
from math import sqrt


@total_ordering
class Point:

    def __init__(self, *args):
        self.coords = self.__get_coords(args)
        self.dim = len(self.coords)

    @property
    def origin(self):
        """A point of all zeros of the same ambient as the current point"""
        return Point([0] * self.dim)

    @property
    def norm(self):
        return self.distance(self.origin)

    def dot(self, other: 'Point'):
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return sum(tuple(map(lambda x, y: x * y, self.coords, other.coords)))

    def distance(self, other: 'Point'):
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return sqrt(sum(tuple(map(lambda x: x * x, self.sub(other).coords))))

    def add(self, other: 'Point'):
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return Point(tuple(map(lambda x, y: x + y, self.coords, other.coords)))

    def sub(self, other: 'Point'):
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return Point(tuple(map(lambda x, y: x - y, self.coords, other.coords)))

    def __eq__(self, other: 'Point'):
        return self.coords == other.coords

    def __ne__(self, other: 'Point'):
        return not (self == other)

    def __lt__(self, other: 'Point'):
        return self.coords < other.coords

    def __repr__(self):
        return str(self.coords)

    @staticmethod
    def __get_coords(args: tuple) -> tuple:
        if len(args) == 1:
            if type(args[0]) is list or type(args[0]) is tuple:
                return tuple(args[0])
            else:
                raise ValueError('Invalid parameter.')
        else:
            if all(isinstance(x, int) for x in args) or all(isinstance(x, float) for x in args):
                return args
            else:
                raise ValueError('Invalid parameter.')

