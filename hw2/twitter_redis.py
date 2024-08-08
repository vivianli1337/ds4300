from Twitterclass import Twitter


def main():
    twitter_cl = Twitter()
    tweets_data = twitter_cl.load_tweets_data()

    # Clear existing data in Redis
    twitter_cl.redis_client.flushall()

    # Load follows data into Redis and get user_ids list
    user_ids = twitter_cl.load_follows_data()
    user_ids_list = list(user_ids)

    # Empty timelines for all users
    twitter_cl.empty_timelines(user_ids_list)

    # Number of tweets processed
    twitter_cl.insert_tweets(tweets_data)

    # Home timelines retrieved
    twitter_cl.refreshTimeline(user_ids_list)


if __name__ == "__main__":
    main()