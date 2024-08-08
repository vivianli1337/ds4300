import redis
import json
import csv
import random
import time
import twitter_apis as tw


class Twitter:
    def __init__(self, host='localhost', port=6379, decode_responses=True):
        self.redis_client = redis.Redis(host=host, port=port, decode_responses=decode_responses)

    def empty_timelines(self, user_ids):
        """ Empties user timelines in Redis by setting each user's timeline to an empty list
        Args:
            - redis_client: instance of the Redis client to connect to
            - user_ids: list of user_ids
        Returns:
            None
        """
        for user_id in user_ids:
            self.redis_client.hset('timelines', user_id, json.dumps([]))


    def load_follows_data(self):
        """ Loads follows data from .csv file into Redis in key/value pairs with USER_ID as key and all of its FOLLOWS as values
        Args:
            - redis_client: instance of the Redis client ot connect to
        Returns:
            - user_ids: set of all user_ids
         """

        user_ids = set()
        follows_data = []
        with open('follows.csv', 'r', newline='', encoding='utf-8') as follows_file:
            follows_reader = csv.DictReader(follows_file)
            for row in follows_reader:
                user_ids.add(int(row["USER_ID"])),
                user_ids.add(int(row["FOLLOWS_ID"])),
                follows_data.append({
                    "user_id": int(row["USER_ID"]),
                    "follows_id": int(row["FOLLOWS_ID"])
                })

        for follow in follows_data:
            follows_key = f"follows:{int(follow['user_id'])}"
            self.redis_client.sadd(follows_key, follow["follows_id"])

        return user_ids


    def load_tweets_data(self):
        """ Loads tweet data from .csv file into Redis and returns a list of tweet dictionaries
        Args:
            - redis_client: instance of the Redis client ot connect to
        Returns:
            - tweets_data: list of tweet dictionaries, each a tweet with a 'user_id' and 'tweet_text' key

        """
        tweets_data = []
        with open('tweet.csv', 'r', newline='', encoding='utf-8') as tweets_file:
            tweets_reader = csv.DictReader(tweets_file)
            for row in tweets_reader:
                tweets_data.append({
                    "user_id": int(row["USER_ID"]),
                    "tweet_text": str(row["TWEET_TEXT"])
                })

        return tweets_data


    def insert_tweets(self, data):
        """Inserts tweets into Redis
        Args:
            - data: file containing tweet data
            - redis_client: instance of the Redis client ot connect to
        Returns:
            None
        """
        # Simulate posting a tweet and measure time
        tweet_count = 0
        start_time = time.time()
        for tweet_data in data:
            tweet_id = self.redis_client.incr("global:tweet_id")
            tweet = {
                "tweet_id": tweet_id,
                "user_id": tweet_data["user_id"],
                "tweet_ts": time.time(),
                "tweet_text": tweet_data["tweet_text"]
            }
            tw.post_tweet(self.redis_client, tweet)
            tweet_count += 1

            # Check elapsed time
            current_time = time.time()
            elapsed_time = current_time - start_time

            # Check when one second has elapsed and break
            if elapsed_time >= 1:
                break

        # Print the result
        print("Number of tweets processed in one second:", tweet_count / elapsed_time)


    def refreshTimeline(self, user_ids):
        """ Simulates users refreshing their home timelines
        Args:
            - user_ids: list of ID of user to refresh home timeline for
            - redis_client: instance of the Redis client to connect to
        Returns:
            None
        """
        start_time = time.time()
        num_home_timelines = 0
        random_user_id = random.choice(user_ids)
        for i in range(10000):
            tw.get_timeline(self.redis_client, random_user_id)
            num_home_timelines += 1

        current_time = time.time()
        elapsed_time = current_time - start_time
        print("Home timelines retrieved per second:", num_home_timelines / elapsed_time)

