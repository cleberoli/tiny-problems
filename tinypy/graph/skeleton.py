import networkx as nx


class Skeleton:

    graph: 'nx.Graph'

    def __init__(self):
        self.graph = nx.Graph()

    @property
    def edges(self):
        return self.graph.edges

    @property
    def nodes(self):
        return self.graph.nodes

    def add_edge(self, i: int, j: int, h: int = None):
        if h is None:
            self.graph.add_edge(i, j)
        else:
            self.graph.add_edge(i, j, h=h)

    def get_edge(self, i: int, j: int, key: str):
        try:
            return self.graph[i][j][key]
        except KeyError as e:
            raise KeyError(f'Invalid key: {e}')

    def get_edges(self, i: int):
        return self.graph.adj[i]
