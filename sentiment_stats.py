# -*- coding: utf-8 -*-

import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
'''
    database : main_db
'''
db = client.main_db

topic = ["politic_sentiment", "tourism_sentiment", "economy_sentiment", \
        "religion_sentiment"]

#set according to above topic
i = 3

#Sentiment values of corrected tweets
def sentiment_stats():
    print "::", topic[0] ,  "::"
    res = db.religion_sentiment.find({}, {'_id' : False})
    cnt_pos, cnt_neg, cnt_ntrl = 0, 0, 0
    for x in res:
        if(x["polarity"] >= 0.20):
            cnt_pos += 1;
        elif(x["polarity"] <= -0.1):
            cnt_neg += 1;
        else:
            cnt_ntrl += 1;

    print "Positive :: %d" % (cnt_pos)
    print "Negative :: %d" % (cnt_neg)
    print "Neutral :: %d" % (cnt_ntrl)


#Single json data consists of all coutries stats (pos, neg, ntrl)
def segregate_country():
    print "::", topic[i] ,  "::"
    result = db.religion_sentiment.find({}, {"_id" : False})
    country_data = {}
    cnt = 0
    for twt in result:
        cnt += 1
        if("place" in twt):
            if("country" in twt["place"]):
                place = twt["place"]["country"]
                #add key if not exist
                if(place not in country_data):
                    country_data[place] = {}
                    country_data[place]["positive"] = 0
                    country_data[place]["negative"] = 0
                    country_data[place]["neutral"] = 0
                #check value of tweet
                if(twt["polarity"] >= 0.20):
                    country_data[place]["positive"] += 1
                elif(twt["polarity"] <= -0.10):
                    country_data[place]["negative"] += 1
                else:
                    country_data[place]["neutral"] += 1
            else:
                pass
        else:
            pass
    #Writing to file
    with open("rel_country.json", "w") as fw:
        json.dump(country_data, fw)
    #Save the Stats in Collection::
    db.religion_country_stats.insert(country_data)
    #print "Inserted Segregated Country Data!!"


# Count number of countries
def count_country():
    result = db.economy_country_stats.find({}, {"_id" : False})
    print "::", topic[i], "::"
    for r in result:
        print  "Total Countries found : %d" % (len(r))


if __name__ == "__main__":
    segregate_country()
    count_country()
    #sentiment_stats()

    print "Stats Complete!!"

