import tweepy

from tweepy import OAuthHandler
from tweepy.streaming import Stream

import json
import re
import os
import time
import pygsheets
from creds import CONSUMER_KEY, CONSUMER_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, SERVICE_FILE
from joblib import dump, load

# Google Sheets Auth
gc = pygsheets.authorize(service_file=SERVICE_FILE)

# Open worksheet
sh = gc.open('DisasterTweets')
wks = sh[0]


# Twitter credentials
# Obtain them from your twitter developer account
consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_KEY_SECRET
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET

# Pass your twitter credentials to tweepy via its OAuthHandler
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

pipe = load('pipe.joblib')


# Crawling starts
def scraptweets(search_words, numTweets):

    program_start = time.time()

    start_run = time.time()

    tweets = tweepy.Cursor(api.search_tweets, q=search_words, lang="en", tweet_mode='extended', result_type='recent').items(numTweets)
    tweet_list = [tweet for tweet in tweets]
    noTweets = 0
    contents = dict()

    for tweet in tweet_list:
    # Pull the values
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:  # Not a Retweet
            text = tweet.full_text

        if pipe.predict([text])[0] == 0:
            continue

        # Skip duplicate tweets
        if str(text) not in contents.keys():
            contents[str(text)] = str(text)
        else:
            continue
        
        username = str(tweet.user.screen_name)
        acctdesc = str(tweet.user.description)
        location = str(tweet.user.location)
        following = str(tweet.user.friends_count)
        followers = str(tweet.user.followers_count)
        totaltweets = str(tweet.user.statuses_count)
        usercreatedts = str(tweet.user.created_at)
        tweetcreatedts = str(tweet.created_at)
        retweetcount = str(tweet.retweet_count)
        hashtags = str(tweet.entities['hashtags'])
            

        
        # Add the 11 variables to the empty list - ith_tweet:
        ith_tweet = [username, acctdesc, location, following, followers, totaltweets,
                    usercreatedts, tweetcreatedts, retweetcount, text, hashtags]

        # Append to Google Sheet
        wks.insert_rows(1, 1, ith_tweet, False)

        noTweets += 1
        
    # Run ended:
    end_run = time.time()
    duration_run = round((end_run-start_run)/60, 2)
    
    print('no. of tweets scraped for is {}'.format(noTweets))
    print('time take to complete is {} mins'.format(duration_run))


search_words = "usa news"
numTweets = 2500
# Call the function scraptweets
scraptweets(search_words, numTweets)

