from typing import Dict

from pymongo.collection import Collection

from tinypy.geometry.point import Point
from tinypy.models.db_model import DBModel
from tinypy.utils.db import INSTANCES


class Instance(DBModel):

    name: str
    type: str
    dimension: int
    size: int
    solutions: Dict[int, Point]

    def __init__(self, name: str, type: str, dimension: int, size: int, solutions: Dict[int, Point] = None):
        self.name = name
        self.type = type
        self.dimension = dimension
        self.size = size
        self.solutions = dict() if solutions is None else solutions

    @classmethod
    def from_doc(cls, doc: dict) -> DBModel:
        instance = Instance(doc['name'], doc['type'], doc['dimension'], doc['size'])
        instance.load_doc(doc)

        return instance

    @classmethod
    def get_collection(cls) -> Collection:
        return INSTANCES

    def load_doc(self, doc: dict):
        self.id = str(doc['_id'])

        for (key, value) in doc['solutions'].items():
            point = Point(value)
            self.solutions[int(key)] = point

    def get_repr(self) -> dict:
        solutions = dict()

        for (key, value) in self.solutions.items():
            solutions[f'{key}'] = list(value.coords)

        return {'name': self.name,
                'type': self.type,
                'dimension': self.dimension,
                'size': self.size,
                'solutions': solutions}

    def get_query(self) -> dict:
        return {'name': self.name}

    def get_update_values(self) -> dict:
        pass
