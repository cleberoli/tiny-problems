from typing import Dict, List

from tinypy.models.db_model import DBModel, CONES


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
    def get_collection(cls) -> str:
        return CONES

    def get_file_name(self) -> str:
        return self.name

    def load_doc(self, doc: dict):
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
