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


# Reads given file and returns an RDD for that file.
def read_file(FILE, sc):
    rdd = sc.textFile(FILE)
    return rdd

