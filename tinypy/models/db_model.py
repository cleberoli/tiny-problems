import json
from abc import ABC, abstractmethod

from bson.objectid import ObjectId

from tinypy.utils.db import add_document, delete_document, get_document, update_document
from tinypy.utils.file import file_exists, get_full_path

CONES = 'cones'
INSTANCES = 'instances'
POLYTOPES = 'polytopes'
SKELETONS = 'skeletons'


class DBModel(ABC):

    @classmethod
    @abstractmethod
    def from_doc(cls, doc: dict) -> 'DBModel':
        pass

    @classmethod
    @abstractmethod
    def get_collection(cls) -> str:
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

    @abstractmethod
    def get_file_name(self) -> str:
        pass

    def get_file_path(self) -> str:
        return get_full_path('files', self.get_collection(), f'{self.get_file_name()}.json')

    def add_doc(self):
        with open(self.get_file_path(), 'w') as file:
            json.dump(self.get_repr(), file)

    def get_doc(self):
        doc = None

        if file_exists(self.get_file_path()):
            with open(self.get_file_path()) as file:
                doc = json.load(file)
                self.load_doc(doc)

        return doc

    # def update_doc(self):
    #     update_document(self.get_collection(), self.get_query(), self.get_update_values())
    #
    # def delete_doc(self):
    #     delete_document(self.get_collection(), {'_id': ObjectId(self.id)})
