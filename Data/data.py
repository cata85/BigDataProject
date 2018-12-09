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


# Creates collection for authors.
def create_authors(DB_NAME, COLLECTION, rdd):
    def insert(iterator):
        client = MongoClient()
        db = client[DB_NAME]
        collection = db[COLLECTION]
        for data in iterator:
            author = data[0]
            subreddits = list(set(data[1]))
            total = len(subreddits)
            row = {'author': author, 'subreddits': subreddits}
            collection.insert_one(row)
    
    rdd.foreachPartition(insert)
    print('Created authors collection!')
    pass


# Creates collection for subreddits.
def create_subreddits(DB_NAME, AUTHOR_COLLECTION, SUBREDDIT_COLLECTION, SUBREDDITS):
    client = MongoClient()
    db = client[DB_NAME]
    author_collection = db[AUTHOR_COLLECTION]
    subreddit_collection = db[SUBREDDIT_COLLECTION]
    for subreddit in SUBREDDITS:
        print(subreddit)
        data = {}
        total = 0
        authors = author_collection.find({'subreddits': {'$elemMatch': {'$in': [subreddit], '$exists': True}}})
        for author in authors:
            _subreddits = author['subreddits']
            for sub in _subreddits:
                if sub != subreddit:
                    data[sub] = data.get(sub, 0) + 1
                    total += 1
        row = {'subreddit': subreddit, 'total': total, 'data': data}
        subreddit_collection.insert_one(row)
    client.close()
    pass

