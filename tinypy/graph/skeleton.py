from typing import Dict, List, Tuple

from networkx import Graph


class Skeleton:
    """Represents the skeleton of a polytope.

    Attributes:
        graph: The skeleton graph.
    """

    graph: Graph

    def __init__(self):
        """Initializes the skeleton graph.
        """
        self.graph = Graph()

    @property
    def edges(self) -> List[Tuple]:
        """Returns the edges of the skeleton.
        """
        edges = list(self.graph.edges)
        edges.sort()
        return edges

    @property
    def nodes(self) -> List[int]:
        """Returns the nodes of the skeleton.
        """
        return list(self.graph.nodes)

    def add_edge(self, i: int, j: int, h: int = None):
        """Adds a new edge to the skeleton graph.

        Args:
            i: First node.
            j: Second node.
            h: Corresponding hyperplane.
        """
        if h is None:
            self.graph.add_edge(i, j)
        else:
            self.graph.add_edge(i, j, h=h)

    def get_edge(self, i: int, j: int, key: str = 'h') -> int:
        """Returns the edge if it exists.

        Args:
            i: First node.
            j: Second node.
            key: Key to data.
        """
        try:
            return self.graph[i][j][key]
        except KeyError as e:
            raise KeyError(f'Invalid key: {e}')

    def get_edges(self, i: int) -> Dict[int, Dict]:
        """Returns the edges adjacent to the given node.

        Args:
            i: The node.
        """
        return self.graph.adj[i]

    def has_edge(self, i: int, j: int) -> bool:
        """Returns whether the skeleton has the given edge.

        Args:
            i: First node.
            j: Second node.
        """
        return self.graph.has_edge(i, j)
