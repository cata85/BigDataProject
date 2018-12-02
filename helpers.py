import findspark
findspark.init()
from itertools import islice
import pymongo
from pymongo import MongoClient
from pyspark import SparkContext


# Initializes the Mongodb client and Spark context.
def initialize():
    client = MongoClient()
    sc = SparkContext('local', 'Project')
    return client, sc

# Checks if a database exists.
def database_exists(client, DB_NAME):
    db_names = client.list_database_names()
    print(db_names)
    if DB_NAME in db_names:
        return True
    return False


# Reads a given file and yields the lines one by one to conserve memory.
# Param 'yield_size' is the size of an array you want to give back when yielded.
# 'yield_size' of 0 will result in one large array. Be careful when using to avoid memory error.
#def read_file(FILE, yield_size=0):
#    with open(FILE, 'r') as _file:
#	if yield_size:
#            return islice(_file, yield_size)
#        return [line for line in _file]

def read_file(FILE, sc):
    rdd = sc.textFile(FILE)
    return rdd

