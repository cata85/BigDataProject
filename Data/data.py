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


# Creates json file to store all data to be used by D3.
def create_json(DB_NAME, SUBREDDIT_COLLECTION, FILENAME):
    client = MongoClient()
    db = client[DB_NAME]
    subreddit_collection = db[SUBREDDIT_COLLECTION]
    data = []
    subreddits = subreddit_collection.find({})
    for sub in subreddits:
        parent_subreddit = sub['subreddit']
        subreddit_data = {'subreddit': parent_subreddit, 'data': {}}
        for key in sorted(sub['data'], key=sub['data'].get, reverse=True):
            child_subreddit = key
            child_total = sub['data'][key]
            subreddit_total = sub['total']
            value = child_total / subreddit_total
            if value < 0.05:
                break
            else:
                subreddit_data['data'][child_subreddit] = value
        data.append(subreddit_data)
    client.close()
    with open(FILENAME, 'w') as json_file:
        json.dump(data, json_file)
    pass

