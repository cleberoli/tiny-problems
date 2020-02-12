from functools import total_ordering

from tinypy.geometry import Point


@total_ordering
class Hyperplane:

    def __init__(self, normal: 'Point', **kwargs, ):
        if len(kwargs) < 1:
            raise ValueError('Invalid parameters.')

        self.normal = normal
        self.d = kwargs.get('d') if 'd' in kwargs else - normal * kwargs.get('p')

    def position(self, p: 'Point'):
        return self.normal * p

    def __eq__(self, other: 'Hyperplane'):
        return self.normal == other.normal and self.d == other.d

    def __ne__(self, other: 'Hyperplane'):
        return not (self == other)

    def __lt__(self, other: 'Hyperplane'):
        return self.normal < other.normal and self.d <= other.d

    def __neg__(self):
        return Hyperplane(-self.normal, d=-self.d)

    def __repr__(self):
        terms = self.__get_terms()
        equation = ' + '.join(terms).replace('+ -', '- ')
        return f'{equation} = {self.d}'

    def __hash__(self):
        return hash(repr(self))

    def __getitem__(self, item: int):
        return self.normal[item]

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
