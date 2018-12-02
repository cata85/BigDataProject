from Data import data
import helpers


# GLOBALS
DB_NAME = 'CIS490'                           # Name of the database that will be used.
PATH = 'file:///home/cata85/CIS490/Project/' # Path of the current working directory
COMMENT_FILE = 'Data/comments.txt'           # Name of the file containing raw comment data.
SUBREDDIT_FILE = 'Data/subreddits.txt'       # Name of thee file containing top 100 subreddits.
COLLECTION = 'subreddits'                    # Name of the collection that will hold all the subreddit data.


def main():
    client, sc = helpers.initialize()
    
    if helpers.database_exists(client, DB_NAME):
        db = data.get_or_create_database(client, DB_NAME)
    else:
        db = data.get_or_create_database(client, DB_NAME)
        subreddits_rdd = helpers.read_file(PATH + SUBREDDIT_FILE, sc)
        data.create_collection(DB_NAME, COLLECTION, subreddits_rdd)
        subreddits_rdd.unpersist()
        comments_rdd = helpers.read_file(PATH + COMMENT_FILE, sc)
        data.update_collection(DB_NAME, COLLECTION, comments_rdd)
        comments_rdd.unpersist()

    # FILL TO GET COLLECTION HERE

    client.close()
    return True


if __name__ == '__main__':
    main()

