from typing import Dict, List, Tuple

from networkx import Graph


class Skeleton:

    graph: 'Graph'

    def __init__(self):
        self.graph = Graph()

    @property
    def edges(self) -> List[Tuple]:
        edges = list(self.graph.edges)
        edges.sort()
        return edges

    @property
    def nodes(self) -> List[int]:
        return list(self.graph.nodes)

    def add_edge(self, i: int, j: int, h: int = None):
        if h is None:
            self.graph.add_edge(i, j)
        else:
            self.graph.add_edge(i, j, h=h)

    def get_edge(self, i: int, j: int, key: str) -> int:
        try:
            return self.graph[i][j][key]
        except KeyError as e:
            raise KeyError(f'Invalid key: {e}')

    def get_edges(self, i: int) -> Dict[int, Dict]:
        return self.graph.adj[i]
