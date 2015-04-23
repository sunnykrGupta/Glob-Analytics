
# coding: utf-8

# In[6]:

import json
import os
from pymongo import MongoClient

client  = MongoClient('localhost', 27017)
db  = client.main_db

#reading from file where data is saved in raw format
path = "../../Glob_Analytics/politics/"
fpath = os.path.join(path, "raw_political_tweets.json")

ifile = open(fpath, 'r')
# list to append all tweets
raw_political_tweets = []

def write_to_db():
    for data in ifile:
        if data != "\n":
            #loading data in proper json format
            parsed_twt = json.loads(data)
            raw_political_tweets.append(parsed_twt)
        else:
            pass
    print " Total lines read :: %d" % (len(raw_political_tweets))
    res = db.raw_politics_data.insert_many(raw_political_tweets)
    ln_id = res.inserted_ids
    print "Total Data inserted into collection :: %d" % (len(ln_id))

if __name__ == "__main__":
    write_to_db()
    #to_check()
