from typing import Dict, List

from pymongo.collection import Collection

from tinypy.geometry.bisection import Bisection
from tinypy.geometry.region import Region
from tinypy.models.db_model import DBModel

from tinypy.utils.db import POSITIONS


class Position(DBModel):

    name: str
    type: str
    region: List[int]
    hash: str
    positions: Dict[int, Bisection]

    def __init__(self, name: str, type: str, region: Region, positions: Dict[int, Bisection] = None):
        self.name = name
        self.type = type
        self.region = region.hyperplanes
        self.hash = repr(region)
        self.positions = dict() if positions is None else positions

    def get_repr(self) -> dict:
        positions = dict()

        for (key, value) in self.positions.items():
            positions[f'{key}'] = [value.left, value.right]

        return {'name': self.name, 'type': self.type, 'region': self.region, 'hash': self.hash, 'positions': positions}

    def get_query(self) -> dict:
        return {'name': self.name, 'hash': self.hash}

    def get_collection(self) -> Collection:
        return POSITIONS

    def load_doc(self, doc: dict):
        for (key, value) in doc['positions'].items():
            bisection = Bisection(value[0], value[1])
            self.positions[int(key)] = bisection

    def get_update_values(self) -> dict:
        doc = self.get_doc()
        new_values = dict()
        current_keys = list(int(k) for k in doc['positions'].keys())
        new_keys = list(key for key in self.positions.keys() if key not in current_keys)

        for key in new_keys:
            new_values[f'positions.{key}'] = [self.positions[key].left, self.positions[key].right]

        return new_values
