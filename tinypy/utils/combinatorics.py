from itertools import combinations, permutations, product
from typing import List


def get_combinations(x: List, r: int) -> List:
    """Returns all possible combinations with r elements.

    Args:
        x: The original set.
        r: Number of elements in a combinations.
    """
    return list(combinations(x, r))


def get_permutations(x: List, repeat: int = None) -> List:
    """Returns all permutations.

    Args:
        x: The original set.
        repeat: Number of possible repetitions.
    """
    x.sort()

    if repeat is None:
        return list(permutations(x))
    else:
        return list(product(x, repeat=repeat))
