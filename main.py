from Data import data
import config
import helpers


def main():
    client, sc, reddit = helpers.initialize()

    # Uses RDD's to parallize initial data processing.
    if config.CREATE_AUTHORS:
        db = data.get_or_create_database(client, config.DB_NAME)
        rdd = helpers.read_file(
                conig.PATH + config.COMMENT_FILE, 
                sc
                )
        rdd2 = rdd.mapPartitions(helpers.mapper)
        rdd3 = rdd2.mapPartitions(helpers.filterer)
        rdd4 = rdd3.reduceByKey(lambda x, y: x + y if y not in x else x) # Returns [(key, [names])]
        data.create_authors(
                config.DB_NAME, 
                config.AUTHOR_COLLECTION, 
                rdd4
                )
        rdd.unpersist()
        rdd2.unpersist()
        rdd3.unpersist()
        rdd4.unpersist()

    # Creates subreddits and the counts of other subreddits used from there.
    if config.CREATE_SUBREDDITS:
        data.create_subreddits(
                config.DB_NAME,
                config.AUTHOR_COLLECTION,
                config.SUBREDDIT_COLLECTION, 
                config.SUBREDDITS
                )

    # Converts the subreddit data to a json data for usage.
    if config.CREATE_JSON:
        data.create_json(
                config.DB_NAME, 
                config.SUBREDDIT_COLLECTION, 
                config.DATA_FILE
                )
    
    # Download subreddit icon images from reddit using reddit's API.
    if config.CREATE_IMAGES:
        helpers.get_subreddit_images(
                reddit, 
                config.SUBREDDITS,
                config.IMAGE_PATH
                )

    client.close()
    return True


if __name__ == '__main__':
    main()

