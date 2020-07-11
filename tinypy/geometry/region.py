from hashlib import blake2b
from typing import List


class Region:
    """Represents a region of the euclidean space delimited by hyperplanes.

    The region consists of all points p, such that the p is in the half-space
    of all delimiting hyperplanes.

    Attributes:
        hyperplanes: Delimiters of the region.

    """

    hyperplanes: List[int]

    def __init__(self, hyperplanes: List[int] = None):
        """Initializes the region.

        The region can be initialized with no hyperplanes (no restrictions).
        The hyperplanes can be added later.

        Args:
            hyperplanes: List of hyperplane indices.
        """
        self.hyperplanes = hyperplanes if hyperplanes is not None else []
        self.hyperplanes = sorted(self.hyperplanes, key=abs)

    def add_hyperplane(self, hyperplane: int):
        """Adds a new hyperplane delimiter, keeping the list sorted.

        Args:
            hyperplane: The hyperplane index.
        """
        self.hyperplanes.append(hyperplane)
        self.hyperplanes = sorted(self.hyperplanes, key=abs)

    def union(self, region: 'Region'):
        """Merges to regions together.

        Args:
            region: The region to be added.

        Returns:
            A new region whose hyperplanes are the union of the current ones and
            the new ones.
        """
        hyperplane_set = set(self.hyperplanes).union(set(region.hyperplanes))
        return Region(sorted(list(hyperplane_set), key=abs))

    def __str__(self):
        return str(self.hyperplanes)

    def __repr__(self):
        h = blake2b(digest_size=20)
        h.update(str.encode(str(self)))
        return h.hexdigest()
