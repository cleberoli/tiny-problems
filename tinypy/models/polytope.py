from pymongo.collection import Collection

from tinypy.models.db_model import DBModel
from tinypy.utils.db import POLYTOPES


class Polytope(DBModel):

    name: str
    type: str
    dimension: int
    solutions: int
    hyperplanes: int
    edges: int
    degree: float

    def __init__(self, name: str, type: str, dimension: int, size: int, hyperplanes: int, edges: int, degree: float):
        self.name = name
        self.type = type
        self.dimension = dimension
        self.solutions = size
        self.hyperplanes = hyperplanes
        self.edges = edges
        self.degree = degree

    @classmethod
    def from_doc(cls, doc: dict) -> DBModel:
        polytope = Polytope(doc['name'], doc['type'], doc['dimension'], doc['solutions'], doc['hyperplanes'], doc['edges'], doc['degree'])

        return polytope

    @classmethod
    def get_collection(cls) -> Collection:
        return POLYTOPES

    def load_doc(self, doc: dict):
        pass

    def get_repr(self) -> dict:
        return {'name': self.name,
                'type': self.type,
                'dimension': self.dimension,
                'solutions': self.solutions,
                'hyperplanes': self.hyperplanes,
                'edges': self.edges,
                'degree': self.degree}

    def get_query(self) -> dict:
        return {'name': self.name}

    def get_update_values(self) -> dict:
        pass
