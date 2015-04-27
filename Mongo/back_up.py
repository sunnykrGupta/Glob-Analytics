# coding: utf-8

import json
import os
from pymongo import MongoClient

client  = MongoClient('localhost', 27017)
main  = client.main_db
back = client.backup_db
raw = client.raw_db

# list to append all tweets
copy_tweets = []

def backup_db():
    twtcnt = 0
    tweets = main.raw_religion_data.find({}, {'_id' : False})
    print "Tweets copying are :: %d" % (tweets.count())

    for tw in tweets:
        copy_tweets.append(tw)

    print " Total tweets to be copy :: %d" % (len(copy_tweets))
    res = raw.raw_religion.insert_many(copy_tweets)
    ln_id = res.inserted_ids
    print "Total Data inserted into collection :: %d" % (len(ln_id))

if __name__ == "__main__":
    backup_db()
    #to_check()
