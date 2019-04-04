import sys
import tweepy
import numpy as np
from textblob import TextBlob

def tweet_analysis(query):
    # get tweets
    tweets = tweepy.Cursor(api.search, q = query + " -filter:retweets").items(20)

    for tweet in tweets:
        phrase = TextBlob(tweet.text)
        polarities = []
        subjectivities = []

        if not is_english(phrase):
            try: 
                phrase = TextBlob(str(phrase.translate(to = "en")))
            except:
                phrase = phrase

        if phrase.sentiment.polarity != 0.0 and phrase.sentiment.subjectivity != 0.0:
            polarities.append(phrase.sentiment.polarity)
            subjectivities.append(phrase.sentiment.subjectivity)

        print("Tweet: " + tweet.text)
        print("Polarity: " + str(phrase.sentiment.polarity))
        print("Subjectivity: " + str(phrase.sentiment.subjectivity))
        print("***************************************")

    return {"polarity": polarities, "subjectivity": subjectivities}

def is_english(text):
    if text.detect_language() == "en":
        return True
    return False

def get_polarity_mean(valid_tweets):
    try: 
        if len(valid_tweets["polarity"]) == 0:
            return 0
            
        return np.mean(valid_tweets["polarity"])
    except:
        return 0

def get_weighted_polarity_mean(valid_tweets):
    try:
        return np.average(valid_tweets["polarity"], weights=valid_tweets["subjectivity"])
    except:
        return 0

def print_result(mean):
    if mean > 0.0:
        print("POSITIVE")
    elif mean == 0.0:
        print("NEUTRAL")
    else:
        print("NEGATIVE")

# make sure consumer keys and access tokens are included in command line call
if len(sys.argv) != 5:
    print("need to add consumer keys and access tokens as command line args")
    exit()

# get consumer keys from command line
consumer_key = sys.argv[1]
consumer_secret = sys.argv[2]

# get access tokens from command line
access_token = sys.argv[3]
access_token_secret = sys.argv[4]

# create auth object for api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# create api object
api = tweepy.API(auth)

query = input("Enter a query to find: ")
analysis = tweet_analysis(query)

print("WEIGHTED MEAN: " + str(get_weighted_polarity_mean(analysis)))
print_result(get_weighted_polarity_mean(analysis))

print("MEAN: " + str(get_polarity_mean(analysis)))
print_result(get_polarity_mean(analysis))
