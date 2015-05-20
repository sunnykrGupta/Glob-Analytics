
# -*- coding: utf-8 -*-

import json
import re
import string
import time
from spell import correct
from textblob import TextBlob
from pymongo import MongoClient


client = MongoClient('localhost', 27017)

'''
    database = 'main_db'
'''
maindb = client.main_db
batchdb = client.batch_db

'''
    tweet_clean remove url and tagged @user from tweets
'''
def tweet_clean(tweet):
    #REGEX for tweet url removal
    tweet = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', tweet)
    #REGEX for @users removal
    tweet = re.sub('@[\w]+' , '', tweet)

    return tweet

'''
    clean_text remove any unicode characters and punctuation
    from tweets to make clean text for sentiment evaluation.
'''
def clean_text(text):
    #REGEX for tweet unicode removal
    text =  re.sub(r'(\\u[0-9A-Fa-f]+)', '', text)

    #Remove punctuation in tweet
    punc = set(string.punctuation)
    text = "".join(c for c in text if c not in punc)

    return text

'''
   This module is imported from spell.py file that used open sourced
   spell correction algorithm using corpus in big.txt file.
   Gives 83+ % accuracy according to Peter Norvig.
'''
def spell_correct(tweet):
    #Spitting the sentence into words
    words = tweet.split()
    text = ""
    for w in words:
        #spell correction module in spell.py
        w = correct(w)
        text += w + " "

    return text


'''
    Function that check if lang is not 'en' ie, english,
    coverts using TextBlob wrapper that uses google translator api.
'''
def process_tweet(tweet, translate):
    #Extract tweet
    tweet_txt = tweet["text"]
    # Removing url, @users
    tweet_txt = tweet_clean(tweet_txt)

    if(translate):
        # Create textblob object for lang translation
        tblob = TextBlob(tweet_txt)
        frm_ln = tweet["lang"]
        print "Conversion from : ", frm_ln
        # Translation of tweets from native lang to 'en'
        tweet_text = tblob.translate(from_lang=frm_ln, to="en")
        text = str(tweet_text)
        #clean the text remove unicode, punctuation
        cleantxt = clean_text(text)
        cleantxt = cleantxt.decode('utf-8')
    else:
        cleantxt = clean_text(tweet_txt)
    #Spell Correctify of tweet
    cleantxt = spell_correct(cleantxt)

    return cleantxt

'''
    Main Function to fetch records from collection and
    apply above operation and get the sentiment score.
'''
def collect_data():
    #Fetch geotagged data from collection
    twts_result = maindb.economy_geolocation.find({}, {'__id' : False})
    print "Tweets for processing -> %d" %(twts_result.count())
    tweets_sentiment = []
    batch_tweets = []
    #Copy the cursor data into list
    tweets_collection = list(twts_result[:])
    cnt = 0
    for twt in tweets_collection:
        #print type(twt["text"])
        cnt += 1
        print "Twt : %d" % (cnt)
        #if(cnt > 15000):
        if(twt['lang'] != 'en' and twt['lang'] != 'und'):
            cleantxt  = process_tweet(twt, True)
            twt["text"] = cleantxt
            cleantxt = TextBlob(cleantxt)
            #Sentiment score of clean tweet
            twt["polarity"] = cleantxt.sentiment.polarity
            #batch_tweets.append(twt)
            tweets_sentiment.append(twt)
        elif(twt['lang'] != 'und'):
            cleantxt = process_tweet(twt, False)
            twt["text"] = cleantxt
            tblob = TextBlob(cleantxt)
            twt["polarity"] = tblob.sentiment.polarity
            #batch_tweets.append(twt)
            tweets_sentiment.append(twt)
        else:
            pass

        if(len(batch_tweets) == 100):
            print "Batch len:: ", len(batch_tweets)
            #batch backup collection insertion [Checkpointing processed data]
            #batchdb.economy_test_sentiment.insert_many(batch_tweets)
            del batch_tweets[:]
            time.sleep(2)
    #Insertion into collection
    #records = maindb.economy_sentiment.insert_many(tweets_sentiment)
    rec_ids  = records.inserted_ids
    print "Inserted tweets after evaluation : %d" % (len(rec_ids))


if __name__ == "__main__":
    collect_data()
    print "GeoTagged Collection Processed Completely!!"
