from itertools import combinations, permutations, product
from typing import List


def get_combinations(x: List, r: int) -> List:
    return list(combinations(x, r))


def get_permutations(x: List, repeat: int = None) -> List:
    x.sort()

    if repeat is None:
        return list(permutations(x))
    else:
        return list(product(x, repeat=repeat))
