from typing import Dict, List, Tuple

from pymongo.collection import Collection

from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.point import Point
from tinypy.models.db_model import DBModel, SKELETONS


class Skeleton(DBModel):

    name: str
    type: str
    dimension: int
    size: int
    nodes: List[int]
    hyperplanes: Dict[int, Hyperplane]
    n_skeleton_hyperplanes: int
    n_complement_hyperplanes: int
    skeleton_edges: List[Tuple[int, int, int]]
    complement_edges: List[Tuple[int, int, int]]

    def __init__(self, name: str, type: str, dimension: int, size: int, nodes: List[int] = None,
                 hyperplanes: Dict[int, Hyperplane] = None, n_skeleton_hyperplanes: int = None, n_complement_hyperplanes: int = None,
                 skeleton_edges: List[Tuple[int]] = None, complement_edges: List[Tuple[int]] = None):
        self.name = name
        self.type = type
        self.dimension = dimension
        self.size = size
        self.nodes = list(range(1, size + 1)) if nodes is None else nodes
        self.hyperplanes = dict() if hyperplanes is None else hyperplanes
        self.n_skeleton_hyperplanes = 0 if n_skeleton_hyperplanes is None else n_skeleton_hyperplanes
        self.n_complement_hyperplanes = 0 if n_complement_hyperplanes is None else n_complement_hyperplanes
        self.skeleton_edges = [] if skeleton_edges is None else skeleton_edges
        self.complement_edges = [] if complement_edges is None else complement_edges

    @classmethod
    def from_doc(cls, doc: dict) -> DBModel:
        skeleton = Skeleton(doc['name'], doc['type'], doc['dimension'], doc['size'])
        skeleton.load_doc(doc)

        return skeleton

    @classmethod
    def get_collection(cls) -> Collection:
        return SKELETONS

    def get_file_name(self) -> str:
        return self.name

    def load_doc(self, doc: dict):
        self.n_skeleton_hyperplanes = doc['n_skeleton_hyperplanes']
        self.n_complement_hyperplanes = doc['n_complement_hyperplanes']

        for (key, value) in doc['hyperplanes'].items():
            hyperplane = Hyperplane(Point(value[:-1]), d=value[-1])
            self.hyperplanes[int(key)] = hyperplane

        for s_edge in doc['skeleton_edges']:
            self.skeleton_edges.append((s_edge[0], s_edge[1], s_edge[2]))

        for c_edge in doc['complement_edges']:
            self.complement_edges.append((c_edge[0], c_edge[1], c_edge[2]))

    def get_repr(self) -> dict:
        hyperplanes = dict()
        skeleton_edges = []
        complement_edges = []

        for (key, value) in self.hyperplanes.items():
            h = list(value.normal.coords) + [value.d]
            hyperplanes[f'{key}'] = h

        for s_edge in self.skeleton_edges:
            skeleton_edges.append(list(s_edge))

        for c_edge in self.complement_edges:
            complement_edges.append(list(c_edge))

        return {'name': self.name,
                'type': self.type,
                'dimension': self.dimension,
                'size': self.size,
                'n_skeleton_hyperplanes': self.n_skeleton_hyperplanes,
                'n_complement_hyperplanes': self.n_complement_hyperplanes,
                'nodes': self.nodes,
                'hyperplanes': hyperplanes,
                'skeleton_edges': skeleton_edges,
                'complement_edges': complement_edges}

    def get_query(self) -> dict:
        return {'name': self.name}

    def get_update_values(self) -> dict:
        pass
