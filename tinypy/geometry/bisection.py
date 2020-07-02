from bisect import insort
from typing import List


class Bisection:

    left: List[int]
    right: List[int]

    def __init__(self, left: List[int] = None, right: List[int] = None):
        self.left = sorted(left) if left is not None else []
        self.right = sorted(right) if right is not None else []

    def add_left(self, left: int):
        insort(self.left, left)

    def add_right(self, right: int):
        insort(self.right, right)

    def __str__(self):
        return str({'left': self.left, 'right': self.right})

    def __repr__(self):
        return str((self.left, self.right))
