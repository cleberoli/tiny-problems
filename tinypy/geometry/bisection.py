from bisect import insort
from typing import List


class Bisection:
    """Represents the bisection of the solutions by a given hyperplane.

    Given a hyperplane this object represents which solution regions don't
    intercept the hyperplane, being completely contained in either side of
    the hyperplane.

    Attributes:
        left: List of solution indices to the left of the hyperplane.
        right: List of solution indices to the right of the hyperplane.
    """

    left: List[int]
    right: List[int]

    def __init__(self, left: List[int] = None, right: List[int] = None):
        """Initializes the bisection.

        The bisection can be initialized with empty lists and the solutions
        can be added later.

        Args:
            left: List of solution indices to the left of the hyperplane.
            right: List of solution indices to the right of the hyperplane.
        """
        self.left = sorted(left) if left is not None else []
        self.right = sorted(right) if right is not None else []

    def add_left(self, left: int):
        """Adds a new solution to the left side, keeping the list sorted.

        Args:
            left: The solution index.
        """
        insort(self.left, left)

    def add_right(self, right: int):
        """Adds a new solution to the right side, keeping the list sorted.

        Args:
            right: The solution index.
        """
        insort(self.right, right)

    def __str__(self):
        return str({'left': self.left, 'right': self.right})

    def __repr__(self):
        return str((self.left, self.right))
