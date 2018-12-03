import json
import pymongo
from pymongo import MongoClient


# Gets or creates the database dependent on whether it exists.
def get_or_create_database(client, DB_NAME):
    db = client[DB_NAME]
    return db


# Returns a specified collection.
def get_collection(db, COLLECTION):
    collection = db[COLLECTION]
    return collection


# Creates collections for subreddits.
def create_collections(DB_NAME, rdd):
    def insert(iterator):
        client = MongoClient()
        db = client[DB_NAME]
        for data in iterator:
            author = data[0]
            subreddits = data[1]
            total = len(subreddits)
            collection = db[subreddit]
            if count % 5000 == 0:
                print(COUNT)
            COUNT += 1
            row = {'author': author, 'subreddits': subreddits}
            collection.insert_one(row)

    rdd.foreachPartition(insert)
    print('Created authors collection!')
    pass


COUNT = 0

