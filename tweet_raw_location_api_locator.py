#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import string
import os
from geopy.geocoders import GoogleV3
from pymongo import MongoClient

#pymongo db operation client connection
client = MongoClient('localhost', 27017)

#Assign api key
api = os.getenv('api_key', None)

#Google map api_key
geolocator = GoogleV3(api_key=api)

#filter these from GoogleV3 json data
require = ["country", "administrative_area_level_1", "administrative_area_level_2"]

def clean_V3_json(data):
    t = {}
    t["location"]  = data["geometry"]["location"]
    t["place"] = {}
    for addr in data["address_components"]:
        #Match types with require list
        if(set(addr["types"]).intersection(require)):
            if(require[0] in addr["types"]):
                t["place"]["country"] = addr["long_name"]
            elif(require[1] in addr["types"]):
                t["place"]["state"] = addr["long_name"]
            elif(require[2] in addr["types"]):
                t["place"]["name"] = addr["long_name"]
        else:
            pass
    #return dataobj
    return t

def find_location(address):
    location = geolocator.geocode(address, language='en')
    time.sleep(1.0)
    if location != None:
        t = clean_V3_json(location.raw)
        return t
    else:
        return False

def data_iterator(r):
    result = None
    if("geo" in r):
        r["location"] = {}
        r["location"]["lat"] = r["geo"]["coordinates"][0]
        r["location"]["lng"] = r["geo"]["coordinates"][1]
        del r["geo"], r["coordinates"]
        if("retweet" in r):
            del r["retweet"]
        return r
    elif("retweet" in r and "geo" in r["retweet"]):
        r["location"] = {}
        r["place"] = {}
        r["location"]["lat"] = r["retweet"]["geo"]["coordinates"][0]
        r["location"]["lng"] = r["retweet"]["geo"]["coordinates"][1]
        r["place"]["country"] = r["retweet"]["country"]
        r["place"]["name"] = r["retweet"]["name"]
        del r["retweet"]
        if("geo" in r):
            del r["geo"], r["coordinates"]
        return r
    else:
        if("location" in r):
            print "Location to V3 :: " , r["location"]
            result = find_location(r["location"])
            if(result == False and "retweet" in r and "location" in r["retweet"]):
                result = find_location(r["retweet"]["location"])
        else:
            if("retweet" in r and "location" in r["retweet"]):
                result = find_location(r["retweet"]["location"])
                print "Retweet_LOC to V3:: ", r["retweet"]["location"]
        if(result != False):
            r["location"] = result["location"]
            r["place"] = result["place"]
            if("retweet" in r):
                del r["retweet"]
            return r
        else:
            return False

#Data receiveing module
def collect_data():
    #store processed tweets
    clean_twt = []
    cnt = 0
    rejected = 0
    db = client.tweets_db
    collection = db.filter_twt.find()
    print "Collection DOC's for processing %d tweets." % (collection.count())
    for raw in collection:
        cnt += 1
        print "Tweet %d ::- " % (cnt)
        '''
        twt = data_iterator(raw)
        if(twt != False):
            clean_twt.append(twt)
        else:
            rejected += 1
            print "Tweet rejected!!"
        '''
    #Data insertion into newdb (collection)
    '''
    db.cleantwt_db.insert_many(clean_twt)
    print "Data Inserted into Collection"
    with open("dump.json", "a") as fw:
        json.dump(clean_twt, fw)
    print "Data Written to file!"
    print "%d Processing Done!!" % (cnt)
    print "%d Tweets Rejected (False location)!!" % (rejected)
    '''

if __name__ == "__main__":
    #write_to_db()
    collect_data()
    #read_process()
