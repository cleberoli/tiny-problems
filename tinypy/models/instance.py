from typing import Dict, List

from pymongo.collection import Collection

from tinypy.models.db_model import DBModel
from tinypy.utils.db import INSTANCES


class Instance(DBModel):

    name: str
    type: str
    dimension: int
    size: int
    points: Dict[int, List[int]]

    def __init__(self, name: str, type: str, dimension: int, size: int, points: Dict[int, List[int]]):
        self.name = name
        self.type = type
        self.dimension = dimension
        self.size = size
        self.points = points

    @classmethod
    def from_doc(cls, doc: dict) -> DBModel:
        instance = Instance(doc['name'], doc['type'], doc['dimension'], doc['size'], doc['points'])
        instance.load_doc(doc)

        return instance

    @classmethod
    def get_collection(cls) -> Collection:
        return INSTANCES

    def load_doc(self, doc: dict):
        self.name = doc['name']
        self.type = doc['type']
        self.dimension = doc['dimension']
        self.size = doc['size']
        self.points = doc['points']

    def get_repr(self) -> dict:
        return {'name': self.name,
                'type': self.type,
                'dimension': self.dimension,
                'size': self.size,
                'points': self.points}

    def get_query(self) -> dict:
        return {'name': self.name}

    def get_update_values(self) -> dict:
        pass
