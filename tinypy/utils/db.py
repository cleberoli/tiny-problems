import pymongo


CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')
DB = CLIENT['tinypy']

POSITIONS = DB['positions']


def get_document(collection: pymongo.collection.Collection, query: dict) -> dict:
    return collection.find_one(query)


def add_document(collection: pymongo.collection.Collection, doc: dict):
    collection.insert_one(doc)


def update_document(collection: pymongo.collection.Collection, query: dict, values: dict):
    collection.update_one(query, {'$set': values})

