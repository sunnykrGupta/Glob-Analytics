#Import the necessary methods from tweepy library
import os
import json
import string
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token = os.getenv('access_token', None)
access_token_secret = os.getenv('access_token_secret', None)
consumer_key = os.getenv('consumer_key', None)
consumer_secret = os.getenv('consumer_secret', None)

i = 0
class streamListen(StreamListener):
    #data receive here
    def on_data(self, data):
        global i
        try:
            print i
            i += 1
            infile = open('raw_political_tweets.json', 'a')
            infile.write(data)
            infile.write('\n')
            infile.close()
            return True
        except BaseException, e:
            print 'failed data,', str(e)
            time.sleep(25)

    def on_error(self, status):
        print status, "API Error !!!"
        if status == 420:
            stream.disconnect()
        return false



def scrape_data(tweet):
    #tweet = json.loads(tweet)
    #tweet = json.dumps(parsed, indent=4)
    #new file for writing wrangle data
    wrfile = open('wrangle_1.csv', 'a')
    if (tweet["coordinates"] == None):
        wrfile.write("coordinates : null ")
    else:
        wrfile.write("coordinates : " + str(tweet["coordinates"]))

    if (tweet["user"]["location"] == ""):
        wrfile.write(" user.location : " + "__")
    else:
        wrfile.write(" user.location : " + str(tweet["user"]["location"]))

    wrfile.write(" user.geo_enabled : " + str(tweet["user"]["geo_enabled"]))

    if (tweet["geo"] == None):
        wrfile.write(" geo : null ")
    else:
        wrfile.write(" geo : " + str(tweet["geo"]))

    if (tweet["place"] == None):
        wrfile.write(" place : null ")
    else:
        wrfile.write(" place : " + str(tweet["place"]))

    wrfile.write("\n")
    wrfile.close()
    #print "More prints :::::"

def wrangle_tweets():
    ifile = open('raw_tweets.csv', 'r')
    for tweet in ifile:
        #print tweet
        #loading data in proper json format
        #beautyfying our json-data
        #b_tweet = json.dumps(parsed, indent=4)
        if (tweet != "\n"):
            tweet = json.loads(tweet)
            #print tweet["created_at"]
            scrape_data(tweet)
        else:
            pass



if __name__ ==  '__main__':
    #This handles Twitter authentication and the connection to Stream API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, streamListen())

    print "Tracking Starts:: Streaming ON"
    '''
    #Data receiving related to Politics, Government
    stream.filter(track=['Government', 'Politics'])
    #Data receiving related to Tourism
    stream.filter(track=['tourism','travel'])
    #Data receiving related to Economy, Market
    stream.filter(track=['economy', 'market'])
    #Data receiving related to Religion and Beliefs
    stream.filter(track=['religion', 'beliefs'])
    '''
