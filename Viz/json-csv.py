
# coding: utf-8

# In[5]:

#To put this into a CSV, csv code adapted from this recipe
#(http://www.palewire.com/posts/2009/03/03/django-recipe-dump-your-queryset-out-as-a-csv-file/)
#of Ben Welsh at the LAT, who helped me do my first work with APIs:
# IMPORTS

#Make Python understand the stuff in a page on the Internet is JSON
import json

# Make Python understand csvs
import csv

# tell computer where to put CSV
outfile_path='tweets.csv'

# open it up, the w means we will write to it
writer = csv.writer(open(outfile_path, 'w'))

#create a list with headings for our columns
headers = ['lang', 'lat', 'lng', 'value', 'country', 'name', 'text', ]

#write the row of headings to our CSV file
writer.writerow(headers)

fr = open("clean_tweet_location.json", "r")

# GET JSON AND PARSE IT INTO DICTIONARY
# We need a loop because we have to do this for every JSON file we grab
#set a counter telling us how many times we've gone through the loop, this is the first time, so we'll set it at 1
i=1
parsed_json = json.load(fr)
print type(parsed_json)

for tweet in parsed_json:
    #run through each item in results, and jump to an item in that dictionary
    #initialize the row
    row = []
    st = None
    #add every 'cell' to the row list, identifying the item just like an index in a list
    row.append(str(tweet['lang'].encode('utf-8')))
    row.append(tweet['location']["lat"])
    row.append(tweet['location']["lng"])
    row.append(tweet['value'])
    if("place" in tweet):
        if("country" in tweet["place"]):
            row.append(str(tweet["place"]['country'].encode('utf-8')))
        else:
            row.append(st)
        if("name" in tweet["place"]):
            row.append(str(tweet["place"]['name'].encode('utf-8')))
        else:
            row.append(st)
    else:
        row.append(st)
        row.append(st)
    row.append(str(tweet['text'].encode('utf-8')))
    #once you have all the cells in there, write the row to your csv
    writer.writerow(row)
