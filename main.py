from Data import data
import helpers


def main():
    client, sc = helpers.initialize()
    
    if not helpers.database_exists(client, helpers.DB_NAME):
        db = data.get_or_create_database(client, helpers.DB_NAME)
        rdd = helpers.read_file(helpers.PATH + helpers.COMMENT_FILE, sc)
        rdd2 = rdd.mapPartitions(helpers.mapper)
        rdd3 = rdd2.mapPartitions(helpers.filterer)
        rdd4 = rdd3.reduceByKey(lambda x, y: x + y if y not in x else x) # Returns [(key, [names])]
        data.create_authors(helpers.DB_NAME, helpers.AUTHOR_COLLECTION, rdd4)
        rdd.unpersist()
        rdd2.unpersist()
        rdd3.unpersist()
        rdd4.unpersist()

    data.create_subreddits(
            helpers.DB_NAME,
            helpers.AUTHOR_COLLECTION,
            helpers.SUBREDDIT_COLLECTION, 
            helpers.SUBREDDITS
            )

    client.close()
    return True


if __name__ == '__main__':
    main()

