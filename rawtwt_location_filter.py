
from pymongo import MongoClient
import json
import string

client = MongoClient('localhost', 27017)
'''
     #Database (tweets_db)
     #collection (filter_twt)
'''
cln_tweets = [] #list to save all tweets

def extract_text(rawtweet):
    txt = {}
    txt["text"] = rawtweet["text"]
    txt["lang"] = rawtweet["lang"]
    txt["people"] = []
    for user in rawtweet["entities"]["user_mentions"]:
        txt["people"].append(user["screen_name"])

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

    #Database (tweets_db)
    db = client.tweets_db

    # Querying all data documents
    raw_twt = db.raw_tweets.find()
    #total tweets in DB
    print "Total documents - ", raw_twt.count()

    for twt in raw_twt:
        #print type(twt)
        rawtweet = twt
        #clean module
        tweet = clean_tweet(rawtweet)
        if(tweet):
            # contains text and user mentions
            twt_text = extract_text(rawtweet)
            # merging location and text object
            for key, val in twt_text.iteritems():
                tweet[key] = val
            #appending single tweet to list
            cln_tweets.append(tweet)

    #writing cleaned relevant data into different collection (filter_twt)
    results = db.filter_twt.insert_many(cln_tweets)
    tot_insertion = results.inserted_ids
    print "Total insertion into (filter_twt) collection :: %d" % (len(tot_insertion))
    print "Process Done....!!!"

'''
Database (tweets_db)
Collection (filter_twt)
'''
def process_db():
    db = client.tweets_db
    ln = db.filter_twt.find().count()
    print "Total docs before %d" % (ln)
    db.filter_twt.remove()
    ln = db.filter_twt.find().count()
    print "Total docs after %d" % (ln)


if __name__ == "__main__":
    read_raw_data()
    #process_db()
