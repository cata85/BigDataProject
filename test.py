import praw
import requests


reddit = praw.Reddit(
    client_id = 'Ff85HPhi6wky5Q',
    client_secret='WQkqCePEiMDybqTzJp-rY2mTLCs',
    user_agent='testscript by /u/cata85'
)
sub = 'pics'
image_path = 'images'
subreddit = reddit.subreddit(sub)
url = subreddit.icon_img
with open(f'{image_path}/{sub}.png', 'wb') as f:
    f.write(requests.get(url).content)

