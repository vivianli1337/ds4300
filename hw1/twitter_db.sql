CREATE SCHEMA `twitter_db` ;

USE twitter_db;

CREATE TABLE TWEET (
    tweet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tweet_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tweet_text VARCHAR(140)
);

CREATE TABLE Follows (
    user_id INT,
    follows_id INT
);



