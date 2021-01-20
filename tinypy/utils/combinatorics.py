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


def get_unique_partitions(n, index=1) -> List[List[int]]:
    partitions = [[n]]

    for i in range(index, n//2 + 1):
        for p in get_unique_partitions(n-i, i):
            partitions.append(p + [i])

    return partitions


def get_distinct_partitions(n) -> List[List[int]]:
    partitions = get_unique_partitions(n)
    distinct_partitions = [partitions[0]]

    for p in partitions[1:]:
        is_distinct = True

        for i in range(len(p) - 1):
            if p[i] == p[i + 1]:
                is_distinct = False
                break

        if is_distinct:
            distinct_partitions.append(p)

    return distinct_partitions
