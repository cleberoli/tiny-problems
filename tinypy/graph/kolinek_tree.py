from typing import Dict

from tinypy.geometry import Point, Hyperplane
from tinypy.polytopes import Polytope


class KolinekTree:

    def __init__(self, polytope: 'Polytope'):
        self.__S = self.__get_hyperplanes(polytope.vertices)
        print(self.__S)

    @staticmethod
    def __get_hyperplanes(vertices: Dict[int, 'Point']):
        hyperplanes = set()

        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                normal = vertices[i] - vertices[j]
                normal.add_coord(0)
                hyperplanes.add(Hyperplane(normal, d=0))

        hyperplanes = list(hyperplanes)
        hyperplanes.sort()
        return dict((key, hyperplanes[key]) for key in range(len(hyperplanes)))
