import json
import pymongo
from pymongo import MongoClient


# Gets or creates the database dependent on whether it exists.
def get_or_create_database(client, DB_NAME):
    db = client[DB_NAME]
    return db


# Returns a specified collection.
def get_collection(db, COLLECTION_NAME):
    collection = db[COLLECTION_NAME]
    return collection


# Creates a collection for the database.
def create_collection(DB_NAME, COLLECTION, rdd):
    def insert(iterator):
        print('inside')
        client = MongoClient()
        db = client[DB_NAME]
        collection = db[COLLECTION]
        for data in iterator:
            json_data = json.loads(data)
            collection.insert_one(json_data)

    rdd.foreachPartition(insert)
    print('done')
    pass

