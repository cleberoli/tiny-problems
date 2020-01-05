from itertools import permutations
from itertools import product
from typing import List


def get_permutations(x: List, repeat: int = None) -> List:
    x.sort()

    if repeat is None:
        return list(permutations(x))
    else:
        return list(product(x, repeat=repeat))
