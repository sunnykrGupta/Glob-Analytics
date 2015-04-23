
from pymongo import MongoClient
import json
import string

'''
     #Database (main_db)
     #collection (politic_fltr)
'''
client = MongoClient('localhost', 27017)

#Database (main_db)
db = client.main_db

cln_tweets = [] #list to save all tweets

#Extract text and lang of tweet
def extract_text(rawtweet):
    txt = {}
    txt["text"] = rawtweet["text"]
    txt["lang"] = rawtweet["lang"]

    return txt


def clean_tweet(tweet):
    t = {}
    #User Tweet location extraction
    if (tweet["coordinates"] != None):
        t["coordinates"] = tweet["coordinates"]
        t["geo"] = tweet["geo"]
        if("place" in tweet):
            t["place"] = {}
            t["place"]["country"] = tweet["place"]["country"]
            t["place"]["name"] = tweet["place"]["name"]
    if(tweet["user"]["location"]):
        t["location"] = tweet["user"]["location"]

    #location of Retweeted User
    retwt = {}
    if ("retweeted_status" in tweet):
        if tweet["retweeted_status"]["coordinates"] != None:
            retwt["coordinates"] = tweet["retweeted_status"]["coordinates"]
            retwt["geo"] = tweet["retweeted_status"]["geo"]
            retwt["place"] = {}
            retwt["place"]["country"]  = tweet["retweeted_status"]["place"]["country"]
            retwt["place"]["name"]  = tweet["retweeted_status"]["place"]["name"]

        if tweet["retweeted_status"]["user"]["location"]:
            retwt["location"] = tweet["retweeted_status"]["user"]["location"]
    else:
        pass
    #check if retweeted has some values then add to main t (json obj)
    if(retwt):
        t["retweet"] = retwt
    return t

def read_raw_data():
    # Querying all data documents
    raw_twt = db.raw_politics_data.find({}, {'__id' : False})
    #total tweets in DB
    print "Total documents - ", raw_twt.count()

    for twt in raw_twt:
        #print type(twt)
        rawtweet = twt
        #clean module
        tweet = clean_tweet(rawtweet)
        if(tweet):
            # contains text and lang
            twt_text = extract_text(rawtweet)
            # merging location and text object
            for key, val in twt_text.iteritems():
                tweet[key] = val
            #appending single tweet to list
            cln_tweets.append(tweet)
        else:
            pass
    #writing cleaned data into collection (politic_filtr)
    results = db.politic_filtr.insert_many(cln_tweets)
    tot_insertion = results.inserted_ids
    print "Total insertion into collection :: %d" % (len(tot_insertion))
    print "Raw Politics Data Filtering Done....!!!"


if __name__ == "__main__":
    read_raw_data()
    #process_db()
