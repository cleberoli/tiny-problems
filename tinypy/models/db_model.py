from abc import ABC, abstractmethod

from pymongo.collection import Collection

from tinypy.utils.db import add_document, get_document, update_document


class DBModel(ABC):

    @abstractmethod
    def get_repr(self) -> dict:
        pass

    @abstractmethod
    def get_query(self) -> dict:
        pass

    @abstractmethod
    def get_update_values(self) -> dict:
        pass

    @abstractmethod
    def get_collection(self) -> Collection:
        pass

    @abstractmethod
    def load_doc(self, doc: dict):
        pass

    def update_doc(self):
        update_document(self.get_collection(), self.get_query(), self.get_update_values())

    def add_doc(self):
        add_document(self.get_collection(), self.get_repr())

    def get_doc(self):
        return get_document(self.get_collection(), self.get_query())
