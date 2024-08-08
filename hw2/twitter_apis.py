import redis
import json


def post_tweet(redis_client, tweet):
    """Posts a tweet in Redis, updating the tweet data and adds it to followers' timelines
    Args:
        - redis_client: instance of the Redis client ot connect to
        - tweet: dict of tweet information
    Returns:
        None
    """

    tweet_key = f"tweet:{tweet['tweet_id']}"
    redis_client.hset(tweet_key, "user_id", tweet["user_id"])
    redis_client.hset(tweet_key, "tweet_ts", tweet["tweet_ts"])
    redis_client.hset(tweet_key, "tweet_text", tweet["tweet_text"])

    # Add tweet to user's home timeline
    followers_key = f"followers:user:{int(tweet['user_id'])}"
    followers = redis_client.smembers(followers_key)
    for follower in followers:
        timeline_key = f"timeline:user:{follower}"
        redis_client.lpush(timeline_key, tweet_key)


def get_timeline(redis_client, user_id, count=10):
    """ Retrieves home timeline for given user
    Args:
        - redis_client: instance of the Redis client ot connect to
        - user_id: ID of user to return home timeline for
        - count: the maximum number of tweets to include in timeline, defaults to 10
    Returns:
        - follows: set of user IDs that the specified user follows
        - tweets: list of tweet dictionaries from tweets in the home timeline
    """
    # Retrieve user IDs that the random user follows
    follows_key = f"follows:{user_id}"
    follows = redis_client.smembers(follows_key)

    # Retrieve tweets from home timeline
    timeline_key = f"timeline:user:{user_id}"
    tweet_keys = redis_client.lrange(timeline_key, 0, count - 1)

    tweets = []
    for tweet_key in tweet_keys:
        tweet = redis_client.hgetall(tweet_key)
        tweets.append(tweet)

    return follows, tweets
