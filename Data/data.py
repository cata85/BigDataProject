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


# Updates the subreddits collection.
def update_collection(DB_NAME, COLLECTION, comments_rdd):
    def insert(iterator):
        client = MongoClient()
        db = client[DB_NAME]
        collection = db[COLLECTION]
        for data in iterator:
            dirty_json = json.loads(data)
            author = dirty_json['author']
            subreddit = dirty_json['subreddit']
            collection.update(
                    {'subreddit': subreddit},
                    {'$addToSet': {'authors': author} },
                    upsert=True)

    comments_rdd.foreachPartition(insert)
    print('Updated subreddits collection')
    pass


# Creates a collection for subreddits.
def create_collection(DB_NAME, COLLECTION, subreddits_rdd):
    def insert(iterator):
        client = MongoClient()
        db = client[DB_NAME]
        collection = db[COLLECTION]
        for _subreddit in iterator:
            row = {'subreddit': _subreddit, 'authors': []}
            collection.insert_one(row)

    subreddits_rdd.foreachPartition(insert)
    print('Created subreddits collection!')
    pass

