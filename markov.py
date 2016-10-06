import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    our_tweet = " ".join(words)
    our_tweet = our_tweet[:123]
    our_tweet = our_tweet.split(" ")
    del our_tweet[-1]
    our_tweet = " ".join(our_tweet)
    our_tweet = our_tweet + " #hbgracefall2016"
    
    return our_tweet



def tweet(our_tweet):
    api = twitter.Api(consumer_key = os.environ["TWITTER_CONSUMER_KEY"], 
        consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"], 
        access_token_key = os.environ["TWITTER_ACCESS_TOKEN_KEY"],
        access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"])
    
    status = api.PostUpdate(our_tweet)

    print status.text

if __name__ == '__main__':
    # Get the filenames from the user through a command line prompt, ex:
    # python markov.py green-eggs.txt shakespeare.txt

    # Open the files and turn them into one long string
    while True:  
        filenames = sys.argv[1:]  

        text = open_and_read_file(filenames)

        # Get a Markov chain
        chains = make_chains(text)

        our_tweet = make_text(chains)

        tweet(our_tweet)

        # Your task is to write a new function tweet, that will take chains as input
        # tweet(chains)
        user_choice = raw_input("Enter to tweet again, q to quit ")
        
        if user_choice == "q":
            break