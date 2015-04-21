
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.tweets_db

#Sentiment values of corrected tweets
def spell_correct_stats():
    res = db.correct_twt_analy.find()
    cnt_pos, cnt_neg, cnt_ntrl = 0, 0, 0
    for x in res:
        if(x["value"] >= 0.20):
            cnt_pos += 1;
        elif(x["value"] <= -0.05):
            cnt_neg += 1;
        else:
            cnt_ntrl += 1;

    print "Positive :: %d" % (cnt_pos)
    print "Negative :: %d" % (cnt_neg)
    print "Neutral :: %d" % (cnt_ntrl)

# Stats of cleaned tweets
def text_cleaned_stats():
    res = db.twt_sentiment.find()
    cnt_pos, cnt_neg, cnt_ntrl = 0, 0, 0
    for x in res:
        if(x["value"] >= 0.20):
            cnt_pos += 1;
        elif(x["value"] <= -0.05):
            cnt_neg += 1;
        else:
            cnt_ntrl += 1;

    print "Positive :: %d" % (cnt_pos)
    print "Negative :: %d" % (cnt_neg)
    print "Neutral :: %d" % (cnt_ntrl)


#Single json data consists of all coutries stats (pos, neg, ntrl)
def segregate_data():
    result = db.twt_sentiment.find({}, {"__id" : False})
    country = {}
    for twt in result:
        if("country" in twt["place"]):
            place = twt["place"]["country"]
            #add key if not exist
            if(place not in country):
                country[place] = {}
                country[place]["positive"] = 0
                country[place]["negative"] = 0
                country[place]["neutral"] = 0
            #check value of tweet
            if(twt["value"] >= 0.20):
                country[place]["positive"] += 1
            elif(twt["value"] <= -0.05):
                country[place]["negative"] += 1
            else:
                country[place]["neutral"] += 1
    db.country_db.insert(country)
    print "Inserted Country Data"


# Count number of countries
def count_country():
    result = db.country_db.find({}, {"__id" : False})
    for r in result:
        print  "Total Countries found in 1000 Tweets : %d" % (len(r.keys()))


if __name__ == "__main__":
    #segregate_data()


