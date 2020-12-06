from abc import ABC, abstractmethod

from pymongo.collection import Collection
from bson.objectid import ObjectId

from tinypy.utils.db import add_document, delete_document, get_document, update_document


class DBModel(ABC):

    id: str

    @classmethod
    def from_id(cls, object_id: str):
        doc = get_document(cls.get_collection(), {'_id': ObjectId(object_id)})
        return cls.from_doc(doc)

    @classmethod
    @abstractmethod
    def from_doc(cls, doc: dict) -> 'DBModel':
        pass

    @classmethod
    @abstractmethod
    def get_collection(cls) -> Collection:
        pass

    @abstractmethod
    def load_doc(self, doc: dict):
        pass

    @abstractmethod
    def get_repr(self) -> dict:
        pass

    @abstractmethod
    def get_query(self) -> dict:
        pass

    @abstractmethod
    def get_update_values(self) -> dict:
        pass

    def add_doc(self):
        self.id = add_document(self.get_collection(), self.get_repr())

    def get_doc(self):
        doc = get_document(self.get_collection(), self.get_query())
        if doc is not None:
            self.load_doc(doc)

        return doc

    def update_doc(self):
        update_document(self.get_collection(), self.get_query(), self.get_update_values())

    def delete_doc(self):
        delete_document(self.get_collection(), {'_id': ObjectId(self.id)})
