from flask import Flask
from flask_restful import Resource, Api

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
from datetime import datetime

app = Flask(__name__)
api = Api(app)

class ScrapeTweets(Resource):
    def get(self):
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

        search_words = "usa news"
        numTweets = 100
        while True:
            try:
                tweets = tweepy.Cursor(api.search_tweets, q=search_words, lang="en", tweet_mode='extended', result_type='recent').items(numTweets)
                tweet_list = [tweet for tweet in tweets]

                contents = set()

                # Start scraping
                for tweet in tweet_list:
                # Pull the values
                    try:
                        text = tweet.retweeted_status.full_text
                    except AttributeError:  # Not a Retweet
                        text = tweet.full_text

                    if pipe.predict([text])[0] == 0:
                        continue

                    # Skip duplicate tweets
                    if str(text) not in contents:
                        contents.add(str(text))
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
                    wks.insert_rows(2, 1, ith_tweet, False)

                wks.update_row(1, ["Last retrieved", str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))], 0)
                # End scraping
            except Exception as e:
                print(str(e))
                break

        return {'status': 200, 'message': 'Scraping done'}


api.add_resource(ScrapeTweets, '/scrape-tweets')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)