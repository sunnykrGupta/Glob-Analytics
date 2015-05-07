
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

db_main = client.main_db
db_batch = client.batch_db

collections = ["politic_final", "tourism_final", "economy_final",
            "religion_final"]

def write_csv():
    #tell computer where to put politic final csv file
    writer_topic = csv.writer(open("politic_final.csv",'wb'))   # Change

    #create a list with headings for our columns
    headers_topic = ['iso2c', 'country','lat', 'lng', 'all', 'score', 'positive', 'negative', 'neutral']

    #write the row of headings to our CSV file
    writer_topic.writerow(headers_topic)
    '''
        fetch the country records from collection
    '''
    results = db_batch.politic_final.find({}, {'_id' :  False})       #Change
    for res in results:
        for con,values in res.iteritems():
            row = []
            row.append(str(values["iso2c"].encode('utf-8')))
            row.append(str(con.encode('utf-8')))
            row.append(values["lat"])
            row.append(values["lng"])
            row.append(values["all"])
            row.append(values["score"])
            row.append(values["positive"])
            row.append(values["negative"])
            row.append(values["neutral"])
            writer_topic.writerow(row)
    print "Final Stats Complete for Visualization!!"


'''
    calculate_score to by formula : prob_positive*3 + prob_neutral*0.5 - prob_negative and taking inverse tangent.
'''
def calculate_score(total, positive, negative, neutral):
    P1 = float(positive)/total
    P2 = float(neutral)/total
    P3 = float(negative)/total
    #print (P1*3)+(P2*0.5) - (P3)
    #Tanget Inverse to calculate_score between [0-1]
    score = tanh( (P1*3)+(P2*0.5) - P3)*10
    return score


def low_tweets_score(v):
    score = calculate_score(v['all'], v['positive'],
        v['negative'], v['neutral'])
    if(score >= 9.00):
        return score*0.7
    elif(score >= 8.00):
        return score*0.8
    elif(score >= 2.00):
        return score*0.8
    elif(score <= 0.0):
        return 3.5
    else:
        return score


'''
    iterator function to score each country::
'''
def score_country():
    #For keeping country score record and sorting to display top countries.
    collections = db_batch.politic_final.find()             #Change
    for record in collections:
        for c,v in record.iteritems():
            if(c != '_id'):                 # By pass ID key of MongoDB
                if(v["all"] <= 50):
                    #provide a constant score to less tweeted country
                    record[c]["score"] = low_tweets_score(v)
                else:
                    # SCORE Calc.
                    score = calculate_score(v["all"], v["positive"], v["negative"], v["neutral"])
                    record[c]["score"] = score
        #Save the changes after processing record keys
        db_batch.politic_final.save(record)                 #Change

    #Save the changed Collection
    write_csv()
    print "Docs score added and data file(csv) created!!"

if __name__ == "__main__":
    score_country()
    print "Country Scoring Complete!"
