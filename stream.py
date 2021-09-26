import string
import praw
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from datetime import datetime
from collections import defaultdict, OrderedDict
import json
from requests import put, get

# Get API credentials from local file
file = open('config.json')
config = json.load(file) 

# Initialize praw
print("Initializing praw")
reddit = praw.Reddit(client_id = config['client_id'],
                     client_secret = config['client_secret'],
                     user_agent = config['user_agent'])

# Set up structure to hold ticker counts
tickers = pd.read_csv("tickers.csv") 
tickers = set(tickers['Symbol'])
tickersDict = dict() # Users that are legit (both old acc and decent karma)
for ticker in tickers:
    tickersDict[ticker] = 0

# Store punctuation marks to be filtered out from ticker content
punct_table = str.maketrans(dict.fromkeys(string.punctuation))

# Configure stream to read r/wsb content
stream = reddit.subreddit("wallstreetbets").stream.comments(skip_existing=True)

print("Starting stream")
# Push stream data to TickerAPI.py
while True:
    comment = next(stream)
    for word in comment.body.split():
        word = word.translate(punct_table) # Remove punctuation 
        if word in tickers:
            print(comment.id, comment.body, word)
            put('http://localhost:5000/', data={'id': comment.id,
                                                'body': comment.body,
                                                'ticker': word
                                                }).json()

