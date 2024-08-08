# import libraries
import pandas as pd
import mysql.connector
import time
import random
import getpass

# Ask user for sensitive credentials for database configuration
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")
database = input("Enter your twitter database:")

# Store credentials
db_config = {
    'host': 'localhost',
    'user': username,
    'password': password,
    'database': database
}

# Iterate through the dataframe and insert tweets into the database
def insert_tweets(df, conn, cursor):
    """
        Inserts tweets from a dataframe into a MySQL database

        Args:
        - df: dataframe containing tweet data
        - conn: MySQL database connection
        - cursor: MySQL database cursor

        Returns:
        None
    """
    # Initialize variables
    start_time = time.time()
    tweet_count = 0
    for index, row in df.iterrows():
        user_id = row['USER_ID']
        tweet_text = row['TWEET_TEXT']

        # Insert tweet into the database and increment tweet count
        cursor.execute("INSERT INTO TWEET (user_id, tweet_text) VALUES (%s, %s)",
                       (user_id, tweet_text))
        tweet_count+=1

        # Check elapsed time
        current_time = time.time()
        elapsed_time = current_time - start_time
        conn.commit()

        # Check when one second has elapsed and break
        if elapsed_time >= 1:
            break

    # Print the result
    print("Number of tweets processed in one second:", tweet_count/elapsed_time)

def get_random_user(df):
    """
        Retrieves a random user ID from the dataframe

        Args:
        - df: dataframe containing user data

        Returns:
        int: Random user ID
    """
    random_user_id = int(random.choice(df['USER_ID']))
    return random_user_id

# Function to retrieve home timeline for a random user
def getTimeline(random_user_id, cursor):
    """
        Retrieves the home timeline for a given user from the database

        Args:
        - random_user_id (int): User ID for whom the home timeline is retrieved
        - cursor: MySQL database cursor

        Returns:
        list: List of tweet texts in the user's home timeline
    """
    cursor.execute(
        "SELECT tweet_text FROM TWEET WHERE user_id IN (SELECT follows_id FROM Follows WHERE follows_id = %s) ORDER BY tweet_ts DESC LIMIT 10",
        (random_user_id,))
    home_timeline = cursor.fetchall()
    return home_timeline

def getFollowers(random_user_id, cursor):
    """
        Retrieves the followers of a given user from the FOLLOWS table in the database

        Args:
        - random_user_id (int): user_id for which to retrieve list of followers
        - cursor: MySQL database cursor

        Returns:
        list: List of follower user IDs
    """
    cursor.execute(
        "SELECT user_id FROM FOLLOWS WHERE follows_id = %s",
        (random_user_id))

    followers = []

    for row in cursor:
        follower = row[0]
        followers.append(follower)

    return followers

def getFollowees(random_user_id, cursor):
    """
        Retrieves the users followed by a given user from the FOLLOWS table in the database

        Args:
        - random_user_id (int): user_id for which to retrieve list of followees
        - cursor: MySQL database cursor

        Returns:
        list: List of followee user IDs
    """
    cursor.execute(
        "SELECT follows_id FROM FOLLOWS WHERE user_id = %s",
        (random_user_id,))

    followees = []
    for row in cursor:
        followee = row[0]
        followees.append(followee)

    return followees

def getTweets(random_user_id, cursor):
    """
       Retrieves tweets posted by a given user from the database

       Args:
       - random_user_id (int): User ID for whom tweets are retrieved
       - cursor (mysql.connector.cursor): MySQL database cursor

       Returns:
       list: List of tweet texts
       """
    cursor.execute(
        "SELECT tweet_text FROM TWEET WHERE user_id = %s",
        (random_user_id))

    tweets = []
    for row in cursor:
        tweets.append(row)

    return tweets

def refreshTimeline(df, conn, cursor):
    """
      Simulates users refreshing their home timelines

      Args:
      - df: dataframe containing user data
      - conn: MySQL database connection
      - cursor: MySQL database cursor

      Returns:
      None
    """
    start_time = time.time()
    num_home_timelines = 0

    # Simulating 10k home timeline refreshes by obtaining a random user each refresh/iteration
    for i in range(10000):
        random_id = get_random_user(df)
        getTimeline(random_id, cursor)
        num_home_timelines += 1

    current_time = time.time()
    elapsed_time = current_time - start_time

    # Closing cursor and calculating timelines per sec
    cursor.close()
    conn.close()
    print("Home timelines retrieved per second:", num_home_timelines / elapsed_time)

def main():
    # Read the file
    tweets_df = pd.read_csv("tweet.csv")

    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Load/refresh tweets and print processed results
    insert_tweets(tweets_df, conn, cursor)
    refreshTimeline(tweets_df, conn, cursor)

main()

