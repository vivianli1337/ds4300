import mysql.connector
import time
import random
import mysql.connector
import time
import random

class TwitterDatabaseManager:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Li2003062303@",
            database="twitter_db"
        )

    def close_db_connection(self):
        self.db_connection.close()

    def postTweet(self, tweet):
        cursor = self.db_connection.cursor()
        query = "INSERT INTO TWEET (user_id, tweet_text) VALUES (%s, %s)"
        cursor.execute(query, (tweet.user_id, tweet.tweet_text))
        self.db_connection.commit()
        cursor.close()

    def getTimeline(self, user_id):
        cursor = self.db_connection.cursor()
        query = """
        SELECT T.tweet_id, T.user_id, T.tweet_text, T.tweet_ts
        FROM TWEET AS T
        INNER JOIN FOLLOWS AS F ON T.user_id = F.follows_id
        WHERE F.user_id = %s
        ORDER BY T.tweet_ts DESC
        LIMIT 10
        """
        cursor.execute(query, (user_id,))
        tweets = [Tweet(*row) for row in cursor]
        cursor.close()
        return tweets
    
    def getFollowers(self, user_id):
        cursor = self.db_connection.cursor()
        query = "SELECT user_id FROM FOLLOWS WHERE follows_id = %s"
        cursor.execute(query, (user_id,))
        followers = [row[0] for row in cursor]
        cursor.close()
        return followers

    def getFollowees(self, user_id):
        cursor = self.db_connection.cursor()
        query = "SELECT follows_id FROM FOLLOWS WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        followees = [row[0] for row in cursor]
        cursor.close()
        return followees

    def getTweets(self, user_id):
        cursor = self.db_connection.cursor()
        query = "SELECT tweet_id, user_id, tweet_text, tweet_ts FROM TWEET WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        tweets = [Tweet(*row) for row in cursor]
        cursor.close()
        return tweets

    def post_tweets_from_file(self, file_path):
        start_time = time.time()
        tweet_count = 0
        cursor = self.db_connection.cursor()

        with open(file_path, 'r') as file:
            next(file)
            for line in file:
                user_id, tweet_text = line.strip().split(",", 1)
                query = "INSERT INTO TWEET (user_id, tweet_text) VALUES (%s, %s)"
                cursor.execute(query, (user_id, tweet_text))
                tweet_count += 1
                self.db_connection.commit()

        duration = time.time() - start_time
        print(f"Time taken to post all tweets: {duration} seconds")
        print(f"Tweets per second: {tweet_count / duration}")
        cursor.close()

    def get_all_user_ids(self):
        cursor = self.db_connection.cursor()
        query = "SELECT DISTINCT user_id FROM TWEET"
        cursor.execute(query)
        user_ids = [row[0] for row in cursor]
        cursor.close()
        return user_ids

    def retrieve_random_timelines(self, num_iterations, user_ids):
        start_time = time.time()

        for _ in range(num_iterations):
            random_user_id = random.choice(user_ids)
            self.getTimeline(random_user_id)

        duration = time.time() - start_time
        print(f"Time taken: {duration} seconds")
        print(f"Timelines per second: {num_iterations / duration}")




class Tweet:
    def __init__(self, tweet_id, user_id, tweet_text, tweet_ts):
        self.tweet_id = tweet_id
        self.user_id = user_id
        self.tweet_text = tweet_text
        self.tweet_ts = tweet_ts7

    def __repr__(self):
        return f"Tweet(tweet_id={self.tweet_id}, user_id={self.user_id}, tweet_text={self.tweet_text}, tweet_ts={self.tweet_ts})"


def main():
    db_manager = TwitterDatabaseManager()
    db_manager.post_tweets_from_file("/Users/vivianli/Documents/ds4300/ds4300Project/tweet.csv")
    user_ids = db_manager.get_all_user_ids()
    db_manager.retrieve_random_timelines(1000, user_ids)
    db_manager.close_db_connection()

if __name__ == "__main__":
    main()
