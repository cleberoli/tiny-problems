from networkx import DiGraph
from typing import List

from tinypy.models.db_model import DBModel, TREES


class Tree(DBModel):
    name: str
    type: str
    graph: DiGraph
    root: str
    height: int
    k: int

    def __init__(self, name: str, type: str, k: int):
        self.name = name
        self.type = type
        self.k = k
        self.graph = DiGraph()
        self.root = ''
        self.height = 0

    def add_node(self, node: str, height: int, solutions: List[int], hyperplane: int):
        self.graph.add_node(node, height=height, solutions=solutions, hyperplane=hyperplane)
        self.height = max(self.height, height)

    def add_edge_left(self, parent: str, child: str):
        self.graph.add_edge(parent, child, direction='left')

    def add_edge_right(self, parent: str, child: str):
        self.graph.add_edge(parent, child, direction='right')

    @classmethod
    def from_doc(cls, doc: dict) -> 'DBModel':
        tree = Tree(doc['name'], doc['type'], doc['k'])
        tree.load_doc(doc)

        return tree

    @classmethod
    def get_collection(cls) -> str:
        return TREES

    def get_file_name(self) -> str:
        return f'{self.name}-k{self.k}'

    def load_doc(self, doc: dict):
        self.height = doc['height']
        self.root = doc['root']
        self.graph = DiGraph()

        for (node, data) in doc['nodes'].values():
            self.add_node(node, data['height'], data['solutions'], data['hyperplane'])

        for edge in doc['edges']:
            if edge[2] == 'left':
                self.add_edge_left(edge[0], edge[1])
            else:
                self.add_edge_right(edge[0], edge[1])

    def get_repr(self) -> dict:
        nodes = dict()
        edges = []

        for n in self.graph.nodes:
            node = self.graph.nodes[n]
            nodes[n] = {'height': node['height'], 'hyperplane': node['hyperplane'], 'solutions': node['solutions']}

        for edge in self.graph.edges.data():
            edges.append((edge[0], edge[1], edge[2]['direction']))

        return {'name': self.name,
                'type': self.type,
                'k': self.k,
                'height': self.height,
                'root': self.root,
                'nodes': nodes,
                'edges': edges}
