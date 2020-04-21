import networkx as nx


class Skeleton:

    def __init__(self):
        self.__graph = nx.Graph()

    @property
    def edges(self):
        return self.__graph.edges

    def get_edge(self, i: int, j: int, key: str):
        try:
            return self.__graph[i][j][key]
        except KeyError as e:
            print(f'Invalid key: {e}')

    def get_edges(self, i: int):
        return self.__graph.adj[i]

    def add_edge(self, i: int, j: int, h: int = None):
        if h is None:
            self.__graph.add_edge(i, j)
        else:
            self.__graph.add_edge(i, j, h=h)
