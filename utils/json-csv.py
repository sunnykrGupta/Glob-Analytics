
import json
import csv
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
'''
 database ::
'''
db_batch = client.batch_db

def write_csv(world):
    #tell computer where to put CSV
    outfile_path = "world_tweets.csv"
    writer = csv.writer(open(outfile_path, 'wb'))

    #create a list with headings for our columns
    headers = ['iso2c', 'country', 'all']

     #write the row of headings to our CSV file
    writer.writerow(headers)
    cnt = 0
    for (country, values) in world.iteritems():
        row = []
        #add every 'cell' to the row list, identifying the item just like an index in a list
        row.append(str(values["iso2c"].encode('utf-8')))
        row.append(str(country.encode('utf-8')))
        row.append(values["all"])
        #once you have all the cells in there, write the row to your csv
        writer.writerow(row)
    print "CSV Records Inserted!!"

def collect_data():
    politic = db_batch.politic_final.find({}, {'_id' : False})
    '''
        To save counter of tweets in all countries in all the four topic
        ['politic', 'tourism'. 'economy', 'religion']
    '''
    world = {}
    #Iterate over politic data
    for pol in politic:
        for c,v in pol.iteritems():
            if(c in world):
                world[c]["all"] += v["all"]
            else:
                world[c] = {}
                world[c]['iso2c'] = v['iso2c']
                world[c]['all'] = v['all']

    tourism = db_batch.tourism_final.find({}, {'_id' : False})
    #Iterate over tourism data
    for tour in tourism:
        for c,v in tour.iteritems():
            if(c in world):
                world[c]["all"] += v["all"]
            else:
                world[c] = {}
                world[c]['iso2c'] = v['iso2c']
                world[c]['all'] = v['all']

    economy = db_batch.economy_final.find({}, {'_id' : False})
    #Iterate over economy data
    for eco in economy:
        for c,v in eco.iteritems():
            if(c in world):
                world[c]["all"] += v["all"]
            else:
                world[c] = {}
                world[c]['iso2c'] = v['iso2c']
                world[c]['all'] = v['all']

    religion = db_batch.religion_final.find({}, {'_id' : False})
    #Iterate over religion data
    for rel in religion:
        for c,v in rel.iteritems():
            if(c in world):
                world[c]["all"] += v["all"]
            else:
                world[c] = {}
                world[c]['iso2c'] = v['iso2c']
                world[c]['all'] = v['all']

    #Pass the overall binded world country data to write in csv format
    write_csv(world)
    print "CSV File Written!"

if __name__ == "__main__":
    collect_data()
    print "CSV File Created!!"
