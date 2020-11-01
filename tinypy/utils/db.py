import pymongo

CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')
DB = CLIENT['tinypy']

INSTANCES = DB['instances']
POSITIONS = DB['positions']
SUBTREES = DB['subtrees']


def get_document(collection: pymongo.collection.Collection, query: dict) -> dict:
    return collection.find_one(query)


def add_document(collection: pymongo.collection.Collection, doc: dict) -> str:
    result = collection.insert_one(doc)
    return result.inserted_id


def update_document(collection: pymongo.collection.Collection, query: dict, values: dict):
    collection.update_one(query, {'$set': values})

