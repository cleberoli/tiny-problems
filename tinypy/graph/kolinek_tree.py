import numpy as np
from typing import Dict

from tinypy.geometry import Point, Hyperplane
from tinypy.polytopes import Polytope


class KolinekTree:

    def __init__(self, polytope: 'Polytope'):
        self.__S = self.__get_hyperplanes(polytope.vertices)
        self.__d = polytope.d

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

    def build(self, p: 'Point'):
        x = list(p.coords)
        x_l = max(x, key=abs)
        l = x.index(x_l)
        A = np.identity(self.__d + 1)
        A[l][l] = 0
        A[l][-1] = 1
        A[-1][l] = np.sign(x_l)
        A_inv = np.linalg.inv(A)
        print(A)
        print(A_inv)
        print(l)
