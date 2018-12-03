import findspark
findspark.init()
from itertools import islice
import pymongo
from pymongo import MongoClient
from pyspark import SparkContext
import json


# Initializes the Mongodb client and Spark context.
def initialize():
    client = MongoClient()
    sc = SparkContext('local', 'Project')
    return client, sc

# Checks if a database exists.
def database_exists(client, DB_NAME):
    db_names = client.list_database_names()
    if DB_NAME in db_names:
        return True
    return False


# Reads given file and returns an RDD for that file.
def read_file(FILE, sc):
    rdd = sc.textFile(FILE)
    return rdd


# Gets a list of the top 100 subreddits.
def get_subreddits(FILE):
    subreddits = []
    with open(FILE) as f:
        for line in f:
            subreddits.append(line[0:len(line)-1])
    return subreddits


# Gathers necessary info from the comment data.
#def get_data(comment_data):
#    jdata = json.loads(comment_data)
#    subreddit = jdata['subreddit']
#    author = jdata['author']
#    return (subreddit, [author])
def get_data(comment_data):
    jdata = json.loads(comment_data)
    subreddit = jdata['subreddit']
    author = jdata['author']
    return (author, [subreddit])


# Mapper for cleaning up all the data within the comment data.
def mapper(iterator):
    return map(lambda x: get_data(x), iterator)


# Filters out the unnecessary data.
def filterer(iterator):
    return filter(lambda x: x[1][0] in SUBREDDITS and x[0] != '[deleted]', iterator)




# GLOBALS
DB_NAME = 'CIS490'                           # Name of the database that will be used.
PATH = 'file:///home/cata85/CIS490/Project/' # Path of the current working directory.
COMMENT_FILE = 'Data/comments.txt'           # Name of the file containing raw comment data.
SUBREDDIT_FILE = 'Data/subreddits.txt'       # Name of thee file containing top 100 subreddits.
COLLECTION = 'authors'                       # Name of the collection that will hold all the subreddit data.
SUBREDDITS = get_subreddits(SUBREDDIT_FILE)
