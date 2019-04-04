import sys
import tweepy
import textblob
import numpy as np

# make sure consumer keys and access tokens are included in command line call
if len(sys.argv) != 5:
    print("need to add consumer keys and access tokens as command line args")
    exit()

# get consumer keys from command line
consumer_key = sys.argv[1]
conumser_secret = sys.argv[2]

# get access tokens from command line
access_token = sys.argv[3]
access_token_secret = sys.argv[4]
