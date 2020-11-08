from typing import Dict, List

from pymongo.collection import Collection

from tinypy.models.db_model import DBModel
from tinypy.utils.db import CONES


class Cone(DBModel):

    name: str
    type: str
    dimension: int
    size: int
    cones: Dict[int, List[int]]

    def __init__(self, name: str, type: str, dimension: int, size: int, cones: Dict[int, List[int]] = None):
        self.name = name
        self.type = type
        self.dimension = dimension
        self.size = size
        self.cones = dict() if cones is None else cones

    @classmethod
    def from_doc(cls, doc: dict) -> DBModel:
        cone = Cone(doc['name'], doc['type'], doc['dimension'], doc['size'])
        cone.load_doc(doc)

        return cone

    @classmethod
    def get_collection(cls) -> Collection:
        return CONES

    def load_doc(self, doc: dict):
        self.id = str(doc['_id'])

        for (key, value) in doc['cones'].items():
            self.cones[int(key)] = value

    def get_repr(self) -> dict:
        cones = dict()

        for (key, value) in self.cones.items():
            cones[f'{key}'] = value

        return {'name': self.name,
                'type': self.type,
                'dimension': self.dimension,
                'size': self.size,
                'cones': cones}

    def get_query(self) -> dict:
        return {'name': self.name}

    def get_update_values(self) -> dict:
        pass
