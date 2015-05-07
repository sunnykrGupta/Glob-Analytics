#! /usr/bin/env python

import csv
import json
from math import tanh
from operator import itemgetter
from pymongo import MongoClient

'''
    database : main_db
'''
client = MongoClient('localhost', 27017)

db_batch = client.batch_db


def sort_apply(country_score):

    # Sort a list of dictionary objects by a key - case sensitive
    mylist = sorted(country_score, key=itemgetter('score'), reverse=True)
    return mylist


def fetch_data():
    results = db_batch.politic_final.find({}, {'_id' : False})      #Change
    print "Docs :: ", results.count()
    docs = []
    for x in results:
        for c,v in x.iteritems():
            obj = {}
            obj['country'] = c
            obj['all'] = v['all']
            obj['positive'] = v['positive']
            obj['negative'] = v['negative']
            obj['neutral'] = v['neutral']
            obj['score'] = v['score']
            docs.append(obj)
    #Sort the countries by score parameter
    top_country = sort_apply(docs)
    for x in top_country:
        print x['country'], x['score']
    cnt = 0
    top = []
    #print type(top_country)
    for x in top_country:
        cnt += 1
        if(cnt > 15):
            break
        else:
            obj = {}
            obj['pos'] = (float(x['positive'])/x['all'])*x['score']
            obj['neg'] = (float(x['negative'])/x['all'])*x['score']
            obj['ntrl'] = (float(x['neutral'])/x['all'])*x['score']
            obj['score'] = x['score']
            obj['country'] = x['country']
            top.append(obj)

    # Write in file
    writer = csv.writer(open("top15_politic.csv", "wb"))        #Change
    #   Write the headers
    header = ['country', 'pos', 'neg', 'ntrl', 'score']
    writer.writerow(header)

    for x in top:
        row = []
        row.append(x['country'])
        row.append(x['pos'])
        row.append(x['neg'])
        row.append(x['ntrl'])
        row.append(x['score'])
        writer.writerow(row)

    print "File Ready for VIZ!"

if __name__ == "__main__":
    fetch_data()
    print "Script Processed!!"
