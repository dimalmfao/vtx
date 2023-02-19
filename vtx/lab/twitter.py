import asyncio
import random
import tweepy
import os

# client = tweepy.Client(os.environ["TWITTERBEARERTOKEN"])

# auth = tweepy.OAuth2BearerHandler(os.environ["TWITTERBEARERTOKEN"])

# client = tweepy.Client(
#     consumer_key="API / Consumer Key here",
#     consumer_secret="API / Consumer Secret here",
#     access_token="Access Token here",
#     access_token_secret="Access Token Secret here",
# )

# api = tweepy.API(auth)

token = os.environ["TWITTERAPIKEY"]
secret = os.environ["TWITTERAPISECRET"]

auth = tweepy.OAuth1UserHandler(token, secret)

api = tweepy.API(auth)

print(auth.get_authorization_url(signin_with_twitter=True))


public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

# token = os.environ["TWITTERAPIKEY"]
# secret = os.environ["TWITTERAPISECRET"]
# key = os.environ["TWITTERBEARERTOKEN"]

# oauth = Twitter.OAuth(token, secret, key)

# t = Twitter(auth=OAuth(token, secret, key, oauth))

# t.statuses.update(status="Hello, world!")
