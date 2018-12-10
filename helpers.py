import findspark
findspark.init()
import config
from itertools import islice
import json
import praw
import pymongo
from pymongo import MongoClient
from pyspark import SparkContext
import requests


# Initializes the Mongodb client and Spark context.
def initialize():
    client = MongoClient()
    sc = SparkContext('local', 'Project')
    reddit = praw.Reddit(
            client_id = 'Ff85HPhi6wky5Q',
            client_secret='WQkqCePEiMDybqTzJp-rY2mTLCs',
            user_agent='/u/cata85'
            )
    return client, sc, reddit


# Reads given file and returns an RDD for that file.
def read_file(FILE, sc):
    rdd = sc.textFile(FILE)
    return rdd


# Gathers necessary info from the comment data.
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
    return filter(lambda x: x[1][0] in config.SUBREDDITS and x[0] != '[deleted]', iterator)


# Downloads subreddit icon images.
def get_subreddit_images(reddit, SUBREDDITS, IMAGE_PATH):
    for subreddit in SUBREDDITS:
        sub = reddit.subreddit(subreddit)
        url = sub.icon_img
        print(f'{subreddit}: {url}')
        if url:
            with open(f'{IMAGE_PATH}/{sub}.png', 'wb') as f:
                f.write(requests.get(url).content)
    pass

