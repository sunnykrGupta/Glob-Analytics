
import json
import re
import collections
import string
from textblob import TextBlob
from pymongo import MongoClient

"""Spelling Corrector.
Copyright 2007 Peter Norvig.
Open source code under MIT license
"""

client = MongoClient('localhost', 27017)
db = client.tweets_db

def words(text): return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
    inserts    = [a + c + b     for a, b in s for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

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
    result = db.twt_sentiment.find({}, {'__id' : False})
    print "Tweets for processing -> %d" %(result.count())
    twt_sentiment = []
    cnt = 0
    for twt in result:
        cnt += 1
        print "Twt : %d" % (cnt)
        words = twt["text"].split()
        text = ""
        for w in words:
            w = correct(w)
            text += w + " "
            twt["text"] = text
        ctxt = TextBlob(text)
        twt["value"] = ctxt.sentiment.polarity
        twt_sentiment.append(twt)

    #insertion into collection
    res = db.correct_twt_analy.insert_many(twt_sentiment)
    ln  = res.inserted_ids
    print "Inserted tweets after evaluation : %d" % (len(ln))

if __name__ == "__main__":
    collect_data()


