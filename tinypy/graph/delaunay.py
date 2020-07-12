from typing import Dict, List, Tuple

from tinypy.graph.skeleton import Skeleton


class DelaunayTriangulation:
    """Represents the Delaunay triangulation.

    Attributes:
        skeleton: The skeleton graph.
    """

    skeleton: Skeleton

    def __init__(self, skeleton: Skeleton = Skeleton()):
        """Initializes the Delaunay triangulation.

        Args:
            skeleton: The skeleton graph.
        """
        self.skeleton = skeleton

    @property
    def edges(self) -> List[Tuple]:
        """Returns the Delaunay edges.
        """
        return self.skeleton.edges

    @property
    def nodes(self) -> List[int]:
        """Returns the Delaunay nodes.
        """
        return self.skeleton.nodes

    def add_edge(self, i: int, j: int, h: int = None):
        """Adds a new edge to the Delaunay graph.

        Args:
            i: First node.
            j: Second node.
            h: Corresponding hyperplane.
        """
        self.skeleton.add_edge(i, j, h)

    def get_edge(self, i: int, j: int, key: str = 'h') -> int:
        """Returns the edge if it exists.

        Args:
            i: First node.
            j: Second node.
            key: Key to data.
        """
        return self.skeleton.get_edge(i, j, key)

    def get_edges(self, i: int) -> Dict[int, Dict]:
        """Returns the edges adjacent to the given node.

        Args:
            i: The node.
        """
        return self.skeleton.get_edges(i)

    def has_edge(self, i: int, j: int) -> bool:
        """Returns whether the Delaunay graph has the given edge.

        Args:
            i: First node.
            j: Second node.
        """
        return self.skeleton.has_edge(i, j)
