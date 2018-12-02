from Data import data
import helpers


# GLOBALS
DB_NAME = 'CIS490'                           # Name of the database that will be used.
PATH = 'file:///home/cata85/CIS490/Project/' # Path of the current working directory
COMMENT_FILE = 'Data/comments.txt'           # Name of the file containing raw comment data.
COMMENT_COLLECTION = 'comments'              # Name of the collection that will hold all the comment data.
COMMENT_DATA = ['author', 'subreddit']       # Data that is wanted from the comment data.


def main():
    client, sc = helpers.initialize()
    print(helpers.database_exists(client, DB_NAME))
    if helpers.database_exists(client, DB_NAME):
        db = data.get_database(client, DB_NAME)
    else:
        db = data.get_or_create_database(client, DB_NAME)
        comment_rdd = helpers.read_file(PATH + COMMENT_FILE, sc)
        data.create_collection(DB_NAME, COMMENT_COLLECTION, COMMENT_DATA, comment_rdd)
    comment_rdd.unpersist()

    client.close()
    return True







if __name__ == '__main__':
    main()

