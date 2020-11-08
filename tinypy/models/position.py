from typing import Dict, List

from pymongo.collection import Collection

from tinypy.geometry.bisection import Bisection
from tinypy.geometry.region import Region
from tinypy.models.db_model import DBModel
from tinypy.utils.db import POSITIONS


class Position(DBModel):

    name: str
    type: str
    hash: str
    region: List[int]
    positions: Dict[int, Bisection]

    def __init__(self, name: str, type: str, region: Region, positions: Dict[int, Bisection] = None):
        self.name = name
        self.type = type
        self.hash = repr(region)
        self.region = region.hyperplanes
        self.positions = dict() if positions is None else positions

    @classmethod
    def from_doc(cls, doc: dict) -> DBModel:
        position = Position(doc['name'], doc['type'], Region(doc['region']))
        position.load_doc(doc)

        return position

    @classmethod
    def get_collection(cls) -> Collection:
        return POSITIONS

    def load_doc(self, doc: dict):
        self.id = str(doc['_id'])

        for (key, value) in doc['positions'].items():
            bisection = Bisection(value[0], value[1])
            self.positions[int(key)] = bisection

    def get_repr(self) -> dict:
        positions = dict()

        for (key, value) in self.positions.items():
            positions[f'{key}'] = [value.left, value.right]

        return {'name': self.name,
                'type': self.type,
                'hash': self.hash,
                'region': self.region,
                'positions': positions}

    def get_query(self) -> dict:
        return {'name': self.name, 'hash': self.hash}

    def get_update_values(self) -> dict:
        doc = self.get_doc()
        self.load_doc(doc)
        new_values = dict()
        current_keys = list(int(k) for k in doc['positions'].keys())
        new_keys = list(key for key in self.positions.keys() if key not in current_keys)

        for key in new_keys:
            new_values[f'positions.{key}'] = [self.positions[key].left, self.positions[key].right]

        return new_values
