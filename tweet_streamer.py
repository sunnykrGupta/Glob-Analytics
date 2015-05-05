
#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
            infile = open('raw_economy_tweets.json', 'a')
            infile.write(data)
            infile.write('\n')
            infile.close()
            return True
        except BaseException, e:
            print 'failed data,', str(e)
            time.sleep(15)

    def on_error(self, status):
        print status, "API Error !!!"
        if status == 420:
            stream.disconnect()
        return false

if __name__ ==  '__main__':
    #This handles Twitter authentication and the connection to Stream API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, streamListen())

    print "Tracking Starts:: Streaming ON"
    '''
    #Data receiving related to Politics, Government
    #stream.filter(track=['Government', 'Politics'])
    #Data receiving related to Tourism
    stream.filter(track=['tourism','travel'])
    #Data receiving related to Economy, Market
    stream.filter(track=['economy', 'market'])
    #Data receiving related to Religion and Beliefs
    stream.filter(track=['religion', 'beliefs'])
    '''
