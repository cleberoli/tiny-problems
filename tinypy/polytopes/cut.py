from typing import Dict

from tinypy.geometry import Point, Hyperplane
from tinypy.polytopes import Polytope


class Cut(Polytope):

    def __init__(self, size: int):
        if size <= 4 or size > 9:
            raise ValueError('The size must be in range(5, 10).')

        Polytope.__init__(self, size, int((size * (size - 1)) / 2), 'cut')

    def get_vertices(self) -> Dict[int, 'Point']:
        switcher = {5: self.__cut_5(), 6: self.__cut_6(), 7: self.__cut_7(), 8: self.__cut_8(), 9: self.__cut_9()}
        vertices = switcher[self.size]

        return dict((key, vertices[key]) for key in range(len(vertices)))

    def get_facets(self) -> Dict[int, 'Hyperplane']:
        return dict()

    @staticmethod
    def __cut_5():
        vertices = [Point(0, 0, 0, 0, 0, 0, 0, 0, 0, 0), Point(1, 1, 1, 1, 0, 0, 0, 0, 0, 0), Point(1, 0, 0, 0, 1, 1, 1, 0, 0, 0),
                    Point(0, 1, 0, 0, 1, 0, 0, 1, 1, 0), Point(0, 0, 1, 0, 0, 1, 0, 1, 0, 1), Point(0, 0, 0, 1, 0, 0, 1, 0, 1, 1),
                    Point(0, 1, 1, 1, 1, 1, 1, 0, 0, 0), Point(1, 0, 1, 1, 1, 0, 0, 1, 1, 0), Point(1, 1, 0, 1, 0, 1, 0, 1, 0, 1),
                    Point(1, 1, 1, 0, 0, 0, 1, 0, 1, 1), Point(1, 1, 0, 0, 0, 1, 1, 1, 1, 0), Point(1, 0, 1, 0, 1, 0, 1, 1, 0, 1),
                    Point(1, 0, 0, 1, 1, 1, 0, 0, 1, 1), Point(0, 1, 1, 0, 1, 1, 0, 0, 1, 1), Point(0, 1, 0, 1, 1, 0, 1, 1, 0, 1),
                    Point(0, 0, 1, 1, 0, 1, 1, 1, 1, 0)]
        return vertices

    @staticmethod
    def __cut_6():
        vertices = [Point(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), Point(1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    Point(1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0), Point(0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0),
                    Point(0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0), Point(0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1),
                    Point(0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1), Point(0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0),
                    Point(1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0), Point(1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0),
                    Point(1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1), Point(1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1),
                    Point(1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0), Point(1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0),
                    Point(1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1), Point(1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1),
                    Point(0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0), Point(0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1),
                    Point(0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1), Point(0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1),
                    Point(0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1), Point(0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0),
                    Point(0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0), Point(0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0),
                    Point(0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1), Point(0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1),
                    Point(1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0), Point(1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1),
                    Point(1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1), Point(1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1),
                    Point(1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1), Point(1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0)]
        return vertices

    @staticmethod
    def __cut_7():
        vertices = []
        return vertices

    @staticmethod
    def __cut_8():
        vertices = []
        return vertices

    @staticmethod
    def __cut_9():
        vertices = []
        return vertices
