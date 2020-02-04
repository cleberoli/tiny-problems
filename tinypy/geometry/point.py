from functools import total_ordering
from math import sqrt


@total_ordering
class Point:

    def __init__(self, *args):
        self.coords = self.__get_coords(args)
        self.dim = len(self.coords)

    @property
    def origin(self):
        """A point of all zeros of the same dimension as the current point"""
        return Point([0] * self.dim)

    @property
    def norm(self):
        return self.distance(self.origin)

    def distance(self, other: 'Point'):
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return sqrt(sum(tuple(map(lambda x: x * x, (self - other).coords))))

    def __lt__(self, other: 'Point'):
        return self.coords < other.coords

    def __gt__(self, other: 'Point'):
        return self.coords > other.coords

    def __eq__(self, other: 'Point'):
        return self.coords == other.coords

    def __ne__(self, other: 'Point'):
        return not (self == other)

    def __add__(self, other: 'Point'):
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return Point(tuple(map(lambda x, y: x + y, self.coords, other.coords)))

    def __sub__(self, other: 'Point'):
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return Point(tuple(map(lambda x, y: x - y, self.coords, other.coords)))

    def __rmul__(self, other):
        if isinstance(other, Point):
            if self.dim != other.dim:
                raise ValueError('The dimensions are not compatible.')

            return sum(tuple(map(lambda x, y: x * y, self.coords, other.coords)))
        elif isinstance(other, int) or isinstance(other, float):
            return Point(tuple(map(lambda x: x * other, self.coords)))

    __mul__ = __rmul__

    def __neg__(self):
        return Point([-c for c in self.coords])

    def __repr__(self):
        return str(self.coords)

    def __hash__(self):
        return hash(repr(self))

    def __getitem__(self, item: int):
        return self.coords[item]

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

