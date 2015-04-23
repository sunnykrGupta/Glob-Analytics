#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import string
import os
from geopy.geocoders import GeoNames
from pymongo import MongoClient


#pymongo db operation client connection
client = MongoClient('localhost', 27017)

#Assign api key
username = os.getenv('osm_username', None)

#OSM map username
geolocator = GeoNames(username=username)

def clean_OSM_json(data):
    t = {}
    #for storing Geo - coordinates
    t["location"]  = {}
    t["location"]["lat"]  = data["lat"]
    t["location"]["lng"]  = data["lng"]

    #place Info
    t["place"] = {}
    if("countryName" in data):
        t["place"]["country"] = data["countryName"]

    if("name" in data):
        t["place"]["name"] = data["name"]

    return t

def find_location(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        time.sleep(1)
        if location != None:
            t = clean_OSM_json(location.raw)
            return t
        else:
            return False
    except:
        print "Error:"
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
        r["place"]["country"] = r["retweet"]["place"]["country"]
        r["place"]["name"] = r["retweet"]["place"]["name"]
        del r["retweet"]
        if("geo" in r):
            del r["geo"], r["coordinates"]
        return r
    else:
        if("location" in r):
            print "Location to OSM :: " , r["location"]
            result = find_location(r["location"])
            if(result == False and "retweet" in r and "location" in r["retweet"]):
                result = find_location(r["retweet"]["location"])
        else:
            if("retweet" in r and "location" in r["retweet"]):
                result = find_location(r["retweet"]["location"])
                print "Retweet_LOC to OSM:: ", r["retweet"]["location"]
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
    fw = open("pol_7.json", "a")
    cnt = 0
    rejected = 0
    db = client.batch_db
    #Fetching from db
    collection = db.pol_7.find({}, {'_id' : False })
    print "Collection DOC's for processing %d tweets." % (collection.count())

    for raw in collection:
        cnt += 1
        print "Tweet %d ::- " % (cnt)
        twt = data_iterator(raw)
        if(twt != False):
            json.dump(twt, fw)
            clean_twt.append(twt)
            db.pol_7_test.insert(twt)
        else:
            rejected += 1
            print "Tweet rejected!!"
    #Data insertion into newdb (collection)
    db.pol_7_loc.insert_many(clean_twt)
    print "Data Inserted into Collection"
    print "%d Processing Done!!" % (cnt)
    print "%d Tweets Rejected (False location)!!" % (rejected)
    fw.close()

if __name__ == "__main__":
    collect_data()
