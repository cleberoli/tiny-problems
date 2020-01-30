from functools import total_ordering

from tinypy.geometry import Point


@total_ordering
class Hyperplane:

    def __init__(self, normal: 'Point', **kwargs):
        if len(kwargs) < 1:
            raise ValueError('Invalid parameters.')

        self.normal = normal
        self.d = kwargs.get('d') if 'd' in kwargs else - normal.dot(kwargs.get('p'))

    @property
    def reflected(self):
        return Hyperplane(self.normal.times(-1), d=self.d)

    def position(self, p: 'Point'):
        return self.normal.dot(p)

    def __eq__(self, other: 'Hyperplane'):
        return self.normal == other.normal and self.d == other.d

    def __ne__(self, other: 'Hyperplane'):
        return not (self == other)

    def __lt__(self, other: 'Hyperplane'):
        return self.normal < other.normal and self.d <= other.d

    def __repr__(self):
        return f'{self.normal}, {self.d}'

    def __hash__(self):
        return hash(repr(self))
