import random

from functools import total_ordering
from math import sqrt
from typing import List, Union


@total_ordering
class Point:
    """Represents a geometrical point in the euclidean space.

    Attributes:
        coords: The point's coordinates.
        dim: The space dimension.
    """

    coords: tuple
    dim: int

    def __init__(self, *args):
        """Initializes the point.

        Args:
            *args: The arguments to initialize the point. It can be a tuple,
                a list, or individual elements (integers or real numbers).
        """
        if type(args[0]) is list or type(args[0]) is tuple:
            args = tuple(args[0])

        if all(isinstance(x, int) for x in args) or all(isinstance(x, float) for x in args):
            self.coords = args
            self.dim = len(self.coords)
        else:
            raise ValueError('Invalid parameter.')

    @classmethod
    def origin(cls, dim: int) -> 'Point':
        """A point of all zeros in the space of given dimension.

        Args:
            dim: The space dimension.

        Returns:
            A point of all zeros in the given dimension.
        """
        return cls([0] * dim)

    @classmethod
    def random(cls, dim: int, a: int = 0, b: int = 1, decimals: int = 0, norm: int = None) -> 'Point':
        """A random point following the given parameters.

        Args:
            dim: The space dimension.
            a: The lower possible value.
            b: The upper possible value.
            decimals: Number of decimal values.
            norm: The desired norm, if any.

        Returns:
            A random point in the given dimension.
        """
        args = [random.randint(a, b) for _ in range(dim)] if decimals == 0 else [round(random.uniform(a, b), decimals) for _ in range(dim)]
        point = cls(args)

        if norm is not None:
            unitary_point = point * (norm / point.norm)
            point = cls([round(i, max(decimals, 4)) for i in unitary_point.coords])

        return point

    @classmethod
    def random_triangle(cls, dim: int, triangles: List[List[int]], a: int = 0, b: int = 1, decimals: int = 4, norm: int = 1) -> 'Point':
        """A random point that respects the triangle inequality constraints.

        Args:
            dim: The space dimension.
            triangles: A list containing the triangles with each triangle being
                represented by a list of three vertices.
            a: The lower possible value.
            b: The upper possible value.
            decimals: Number of decimal values.
            norm: The desired norm, if any.

        Returns:
            A random point in the given dimension that respects the triangle
            inequality.
        """
        point = cls.random(dim, a, b, decimals)

        while not point.respects_triangle_inequality(triangles):
            point = cls.random(dim, a, b, decimals)

        unitary_point = point * (norm / point.norm)
        unitary_point = cls([round(i, max(decimals, 4)) for i in unitary_point.coords])

        return unitary_point

    @property
    def homogeneous_coords(self) -> tuple:
        """Returns the homogeneous coordinates for the point.
        """
        return self.coords + (1, )

    @property
    def norm(self) -> float:
        """Returns the norm for the point.
        """
        return self.distance(self.origin(self.dim))

    def distance(self, other: 'Point') -> float:
        """Returns the distance between two points.

        Args:
            other: The other point.

        Returns:
            The distance between the current point and the given one.
        """
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return sqrt(sum(list(map(lambda x: x * x, (self - other).coords))))

    def respects_triangle_inequality(self, triangles: List[List[int]]):
        """Returns whether the current point respects the triangle inequality.

        Args:
            triangles: A list containing the triangles with each triangle being
                represented by a list of three vertices.
        """
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
