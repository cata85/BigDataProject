import findspark
findspark.init()
import config
from itertools import islice
import json
import praw
import pymongo
from pymongo import MongoClient
from pyspark import SparkContext
from PIL import Image, ImageDraw, ImageFont
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
        else:
            W, H = (256, 256)
            msg = str(sub)
            img = Image.new('RGBA', (W, H), '#e0e1e2')
            draw = ImageDraw.Draw(img)
            my_font = ImageFont.truetype('/home/cata85/ms-fonts/Arial.TTF', 40)
            w, h = my_font.getsize(msg)
            draw.text(((W-w)/2, (H-h)/2), msg, fill='black', font=my_font)
            img.save(IMAGE_PATH + '/' + str(sub) + '.png')
    pass

