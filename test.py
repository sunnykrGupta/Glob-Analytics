#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
from math import fabs
from spell import correct
from scoring_country import calculate_score
from Mongo.rawtwt_location_filter import tweet_filter
from text_clean_sentiment import tweet_clean, clean_text



def test_score_calculate():
    allowed_err = 1e-05

    #Standard Input for test
    input = [100, 40, 23, 37]
    #Expected Output Score
    output = 8.19403710594

    result = calculate_score(input[0], input[1], input[2], input[3])

    if(fabs(result - output) <= allowed_err):
        print "Scoring Module Ok......."
    else:
        print "Failed Scoring Module !! Not Ok!!......"

def test_spell():
    # Input Set of incorrect words
    input_word = ["havv", "guud", "establsh", "schuol"]
    # Outcome of corresponding incorrect input words
    outcome = ["have", "good", "establish", "school"]

    flag = True
    for i in range(4):
        if(outcome[i] == correct(input_word[i])):
            pass
        else:
            flag = False

    if (flag):
        print "Spell Correction Ok......."
    else:
        print "Failed Spell Correction !! Not Ok!!......."

def test_tweet_clean():

    input_tweet = "Stanford Stage rocked by @Adil_07 ramp the show Log on to http://showadil.org and  @Stanford @LiveConcert watch the incredible evening."

    outcome = "Stanford Stage rocked by  ramp the show Log on to  and    watch the incredible evening."

    if(outcome == tweet_clean(input_tweet)):
        print "Tweet Clean Ok........"
    else:
        print "Failed Tweet Clean !! Not OK !!"

def test_clean_text():
    input_tweet = "Stanford Stage, rocked by @adeel ramp the show. Log on \u1220 to and its \u123123time to rock again. #Roge, #RockNight."

    outcome = "Stanford Stage rocked by adeel ramp the show Log on  to and its time to rock again Roge RockNight"

    #print clean_text(input_tweet)

    if(outcome == clean_text(input_tweet)):
        print "Clean Text Ok........"
    else:
        print "Failed Clean Text!! Not OK !!"

def test_tweet_filter():

    output_json =   {
                        'location': u'Washington, DC',
                        'retweet': {
                            'location': u'London'
                        },
                    }

    with open("sample.json", "r") as fr:
        for twt in fr:
            sample_twt = json.loads(twt)
            t_json =  tweet_filter(sample_twt)
            if(t_json == output_json):
                print "Tweet Filter Ok........"
            else:
                print "Failed Tweet Filter!! Not OK !!"





if __name__ == "__main__":

    print "\n \t <--------------- Test Started-----------------> \n"
    print "\n1) Testing Score Calculator :"
    test_score_calculate()
    print "\n2) Testing Spell Corrector Module :"
    test_spell()
    print "\n3) Testing Tweet Clean :"
    test_tweet_clean()
    print "\n4) Testing Clean Text:"
    test_clean_text()
    print "\n5) Testing Tweet Filter:"
    test_tweet_filter()
    print "\n\t <--------------- Testing Over!!-----------------> \n"
