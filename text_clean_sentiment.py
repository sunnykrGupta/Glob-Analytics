
import json
import re
import string
from textblob import TextBlob
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.tweets_db

def clean_text(text):
    #url remove
    #print text
    text = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', text)
    #unicode removal
    text =  re.sub(r'(\\u[0-9A-Fa-f]+)', '', text)
    # Remove @users
    text = re.sub('@[\w]+' , '', text)
    #remove punctuation
    punc = set(string.punctuation)
    text = "".join(c for c in text if c not in punc)
    return text

def collect_data():
    result = db.text_db.find({}, {'__id' : False})
    print "Tweets for processing -> %d" %(result.count())
    twt_sentiment = []
    cnt = 0
    for twt in result:
        #print type(twt["text"])
        cnt += 1
        print "Twt : %d" % (cnt)
        if(twt['lang'] != 'en' and twt['lang'] != 'und'):
            tblob = TextBlob(twt["text"])
            frm_ln = twt["lang"]
            print "Conversion from : ", frm_ln
            text = tblob.translate(from_lang=frm_ln, to="en")
            tmp = str(text)
            ctxt = clean_text(tmp)
            ctxt = ctxt.decode('utf-8')
            print ctxt
            twt["text"] = ctxt
            ctxt = TextBlob(ctxt)
            twt["value"] = ctxt.sentiment.polarity
            twt_sentiment.append(twt)
        elif(twt['lang'] != 'und'):
            text = clean_text(twt["text"])
            twt["text"] = text
            tblob = TextBlob(text)
            twt["value"] = tblob.sentiment.polarity
            twt_sentiment.append(twt)
        else:
            pass
    #insertion into collection
    res = db.twt_sentiment.insert_many(twt_sentiment)
    ln  = res.inserted_ids
    print "Inserted tweets after evaluation : %d" % (len(ln))

if __name__ == "__main__":
    collect_data()


