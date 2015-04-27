# coding: utf-8

import json
import os
from pymongo import MongoClient

client  = MongoClient('localhost', 27017)
db  = client.main_db

#reading from file where data is saved in raw format
path = "../../Glob_Analytics/Tourism/"
fpath = os.path.join(path, "raw_tourism_tweets.json")

ifile = open(fpath, 'r')
# list to append all tweets
raw_tourism_tweets = []


def write_to_db():
    twtcnt = 0
    for data in ifile:
        if data != "\n" and twtcnt <= 26000:
            #loading data in proper json format
            parsed_twt = json.loads(data)
            raw_tourism_tweets.append(parsed_twt)
            twtcnt += 1
        else:
            pass
    print " Total lines read :: %d" % (len(raw_tourism_tweets))
    #res = db.raw_tourism_data_2.insert_many(raw_tourism_tweets)
    ln_id = res.inserted_ids
    print "Total Data inserted into collection :: %d" % (len(ln_id))

if __name__ == "__main__":
    write_to_db()
    ifile.close()
    #to_check()
