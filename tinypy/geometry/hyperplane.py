from functools import total_ordering

from tinypy.geometry.point import Point


@total_ordering
class Hyperplane:

    normal: 'Point'
    d: int

    def __init__(self, normal: 'Point', **kwargs):
        if 'd' not in kwargs and 'p' not in kwargs:
            raise ValueError('Invalid parameters.')

        if 'd' in kwargs and not (isinstance(kwargs['d'], int) or isinstance(kwargs['d'], float)):
            raise ValueError('Invalid parameters.')

        if 'p' in kwargs and not isinstance(kwargs['p'], Point):
            raise ValueError('Invalid parameters.')

        self.normal = normal
        self.d = kwargs.get('d') if 'd' in kwargs else - normal * kwargs.get('p')

    def position(self, p: 'Point'):
        return self.normal * p

    def in_halfspace(self, p: 'Point'):
        return self.normal * p >= self.d

    def __neg__(self):
        return Hyperplane(-self.normal, d=-self.d)

    def __getitem__(self, item: int):
        return self.normal[item]

    def __hash__(self):
        return hash(repr(self))

    def __lt__(self, other: 'Hyperplane'):
        return self.normal < other.normal or self.normal <= other.normal and self.d < other.d

    def __gt__(self, other: 'Hyperplane'):
        return not (self <= other)

    def __eq__(self, other: 'Hyperplane'):
        return self.normal == other.normal and self.d == other.d

    def __ne__(self, other: 'Hyperplane'):
        return not (self == other)

    def __str__(self):
        terms = self.__get_terms()
        equation = ' + '.join(terms).replace('+ -', '- ')
        return f'{equation} = {self.d}'

    def __repr__(self):
        return str(self.normal.coords + (self.d, ))

    def __get_terms(self):
        terms = []

        for d in range(self.normal.dim):
            coefficient = self.normal[d]

            if coefficient != 0:
                if coefficient == 1:
                    terms.append(f'x{d + 1}')
                elif coefficient == -1:
                    terms.append(f'-x{d + 1}')
                else:
                    terms.append(f'{coefficient}x{d + 1}')

        return terms
