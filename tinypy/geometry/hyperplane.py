from tinypy.geometry import Point


class Hyperplane:

    def __init__(self, normal_vector: 'Point', **kwargs):
        if len(kwargs) < 1:
            raise ValueError('Invalid parameters.')

        self.normal_vector = normal_vector
        self.d = kwargs.get('d') if 'd' in kwargs else normal_vector.dot(kwargs.get('p'))

        print(self.d)
