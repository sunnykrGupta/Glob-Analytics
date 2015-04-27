#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import string
import os
from geopy.geocoders import Yandex
from pymongo import MongoClient


#pymongo db operation client connection
client = MongoClient('localhost', 27017)

#Yandex map
geolocator = Yandex(lang='en_US')


# 8703 check db how much data has been written [write from file]
def clean_yandex_json(data, geo):
    t = {}
    #for storing Geo - coordinates
    t["location"]  = {}
    t["location"]["lat"]  = geo[0]
    t["location"]["lng"]  = geo[1]

    #place Info
    t["place"] = {}
    address = data["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]
    if("CountryName" in address):
        t["place"]["country"] = address["CountryName"]

    if("AddressLine" in address):
        t["place"]["name"] = address["AddressLine"].split(",")[-1].strip(" ")

    return t


def find_location(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        time.sleep(1)
        if location != None:
            geo = []
            geo.append(location.latitude)
            geo.append(location.longitude)
            t = clean_yandex_json(location.raw, geo)
            return t
        else:
            return False
    except:
        print "Caught Exception !!!!:"
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
    fw = open("tour_3.json", "a")
    cnt = 0
    rejected = 0
    db_b = client.batch_db
    #db_m = client.main_db
    #Fetching from db
    collection = db_b.col_1.find({}, {'_id' : False })
    #collection = db_m.t_tourism_filter.find({}, {'_id' : False })
    print "Collection DOC's for processing %d tweets." % (collection.count())

    for raw in collection:
        cnt += 1
        print "Tweet %d ::- " % (cnt)
        #if(cnt > 4488):
        twt = data_iterator(raw)
        if(twt != False):
            json.dump(twt, fw)
            clean_twt.append(twt)
            db_b.col_1_test.insert(twt)
        else:
            rejected += 1
            print "Tweet rejected!!"
    #Data insertion into newdb (collection)
    db_b.col_1_loc.insert_many(clean_twt)
    print "Data Inserted into Collection"
    print "%d Processing Done!!" % (cnt)
    print "%d Tweets Rejected (False location)!!" % (rejected)
    fw.close()

if __name__ == "__main__":
    collect_data()

