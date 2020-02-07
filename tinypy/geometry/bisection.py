from bisect import insort
from typing import List


class Bisection:

    def __init__(self, left: List[int] = None, right: List[int] = None):
        self.__left = left if left is not None else []
        self.__right = right if right is not None else []

    @property
    def left(self):
        return self.__left

    @property
    def right(self):
        return self.__right

    def add_left(self, left: int):
        insort(self.__left, left)

    def add_right(self, right: int):
        insort(self.__right, right)

    def remove(self, item):
        if item in self.__left:
            self.__left.remove(item)

        if item in self.__right:
            self.__right.remove(item)

    def __repr__(self):
        return str({'left': self.__left, 'right': self.__right})
