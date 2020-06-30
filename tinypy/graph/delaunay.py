from typing import Dict, List, Tuple

from tinypy.graph.skeleton import Skeleton


class DelaunayTriangulation:

    skeleton: Skeleton

    def __init__(self, skeleton: Skeleton = Skeleton()):
        self.skeleton = skeleton

    @property
    def edges(self) -> List[Tuple]:
        return self.skeleton.edges

    @property
    def nodes(self) -> List[int]:
        return self.skeleton.nodes

    def add_edge(self, i: int, j: int, h: int = None):
        self.skeleton.add_edge(i, j, h)

    def get_edge(self, i: int, j: int, key: str) -> int:
        return self.skeleton.get_edge(i, j, key)

    def get_edges(self, i: int) -> Dict[int, Dict]:
        return self.skeleton.get_edges(i)
