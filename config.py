import helpers


# Gets a list of the top 100 subreddits.
def get_subreddits(FILE):
    subreddits = []
    with open(FILE) as f:
        for line in f:
            subreddits.append(line.rstrip())
    return subreddits


# SETTINGS
CREATE_AUTHORS = False
CREATE_SUBREDDITS = False
CREATE_JSON = False
CREATE_IMAGES = True

# GLOBALS
DB_NAME = 'CIS490'                           # Name of the database that will be used.
PATH = 'file:///home/cata85/CIS490/Project/' # Path of the current working directory.
IMAGE_PATH = 'website/static/images'         # Path of the image directory.
COMMENT_FILE = 'Data/comments.txt'           # Name of the file containing raw comment data.
SUBREDDIT_FILE = 'Data/subreddits.txt'       # Name of the file containing top 100 subreddits.
DATA_FILE = 'Data/data.json'                 # Name of the file containing data for D3.
AUTHOR_COLLECTION = 'authors'                # Name of the collection that will hold all the authors.
SUBREDDIT_COLLECTION = 'subreddits'          # Name of the collection that will hold all the subreddits.
SUBREDDITS = get_subreddits(SUBREDDIT_FILE)  # List that holds the top 100 subreddits.

