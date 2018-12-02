import findspark
findspark.init()
from pyspark import SparkContext
import json


def load_subreddits():
    subreddits = []
    with open('Data/subreddits.txt') as f:
        for line in f:
            subreddits.append(line[0:len(line)-1])
    return subreddits


def get_data(x):
    jdata = json.loads(x)
    subreddit = jdata['subreddit']
    author = jdata['author']
    return (subreddit, [author])


def first(iterator):
    return map(lambda x: get_data(x), iterator)


def second(iterator):
    return filter(lambda x: x[0] in subreddits and '[deleted]' not in x[1], iterator)


sc = SparkContext('local', 'test')
subreddits = load_subreddits()
rdd = sc.textFile('file:///home/cata85/CIS490/Project/Data/comments.txt', 5)
rdd2 = rdd.mapPartitions(first)
rdd3 = rdd2.mapPartitions(second)
rdd4 = rdd3.reduceByKey(lambda x, y: x + y if y not in x else x) # Returns [(key, [names])]

