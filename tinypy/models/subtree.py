from typing import List, Union

from pymongo.collection import Collection

from tinypy.geometry.region import Region
from tinypy.models.db_model import DBModel
from tinypy.utils.constants import ID_SIZE
from tinypy.utils.db import SUBTREES


class Subtree(DBModel):

    name: str
    type: str
    hash: str
    region: List[int]
    solutions: List[int]
    hyperplanes: List[int]

    hyperplane: int
    height: int
    left: Union[int, str]
    right: Union[int, str]

    threshold: int
    unexplored: List[int]

    def __init__(self, name: str, type: str, region: Region, solutions: List[int], hyperplanes: List[int]):
        self.name = name
        self.type = type
        self.hash = repr(region)
        self.region = region.hyperplanes
        self.solutions = solutions
        self.hyperplanes = hyperplanes
        self.unexplored = hyperplanes.copy()

    @classmethod
    def from_doc(cls, doc: dict) -> DBModel:
        subtree = Subtree(doc['name'], doc['type'], Region(doc['region']), doc['solutions'], doc['hyperplanes'])
        subtree.load_doc(doc)

        return subtree

    @classmethod
    def get_collection(cls) -> Collection:
        return SUBTREES

    def load_doc(self, doc: dict):
        self.id = str(doc['_id'])
        self.hyperplane = doc['hyperplane']
        self.height = doc['height']
        self.left = int(doc['left']) if len(str(doc['left'])) < ID_SIZE else str(doc['left'])
        self.right = int(doc['right']) if len(str(doc['right'])) < ID_SIZE else str(doc['right'])
        self.threshold = doc['threshold']
        self.unexplored = doc['unexplored']

    def get_repr(self) -> dict:
        return {'name': self.name,
                'type': self.type,
                'hash': self.hash,
                'region': self.region,
                'solutions': self.solutions,
                'hyperplanes': self.hyperplanes,
                'hyperplane': self.hyperplane,
                'height': self.height,
                'left': self.left,
                'right': self.right,
                'threshold': self.threshold,
                'unexplored': self.unexplored}

    def get_query(self) -> dict:
        return {'name': self.name, 'hash': self.hash}

    def get_update_values(self) -> dict:
        pass
