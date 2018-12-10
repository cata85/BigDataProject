import pymongo
from pymongo import MongoClient


client = MongoClient()
db = client['CIS490']
connection = db['subreddits']
subreddits = connection.find()

for sub in subreddits:
    count = 0
    print('===================================================')
    print(sub['subreddit'])
    for key in sorted(sub['data'], key=sub['data'].get, reverse=True):
        if count == 5:
            break
        count += 1
        print(key + ': ' + str(sub['data'][key] / sub['total']))
    print('===================================================')

client.close()

