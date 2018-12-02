from Data import data
import helpers


# GLOBALS
# DB_NAME = 'CIS490'                           # Name of the database that will be used.
# PATH = 'file:///home/cata85/CIS490/Project/' # Path of the current working directory
# COMMENT_FILE = 'Data/comments.txt'           # Name of the file containing raw comment data.
# SUBREDDIT_FILE = 'Data/subreddits.txt'       # Name of thee file containing top 100 subreddits.
# COLLECTION = 'subreddits'                    # Name of the collection that will hold all the subreddit data.


def main():
    client, sc = helpers.initialize()
    
    if helpers.database_exists(client, helpers.DB_NAME):
        db = data.get_or_create_database(client, helpers.DB_NAME)
    else:
        db = data.get_or_create_database(client, helpers.DB_NAME)
        # subreddits = helpers.get_subreddits(SUBREDDIT_FILE)
        # data.create_collection(DB_NAME, COLLECTION, subreddits_rdd)
        rdd = helpers.read_file(helpers.PATH + helpers.COMMENT_FILE, sc)
        rdd2 = rdd.mapPartitions(helpers.mapper)
        rdd3 = rdd2.mapPartitions(helpers.filterer)
        rdd4 = rdd3.reduceByKey(lambda x, y: x + y if y not in x else x) # Returns [(key, [names])]
        # data.update_collection(DB_NAME, COLLECTION, comments_rdd)
        data.create_collection(helpers.DB_NAME, helpers.COLLECTION, rdd4)
        rdd.unpersist()
        rdd2.unpersist()
        rdd3.unpersist()
        rdd4.unpersist()

    # FILL TO GET COLLECTION HERE

    client.close()
    return True


if __name__ == '__main__':
    main()

