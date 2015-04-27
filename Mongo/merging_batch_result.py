

import json
import os
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
'''
    Database :: (from)batch_db, (to)main_db
    Collection :: (from) pol_*_loc , (to ) pol_geolocation
'''
db_batch = client.batch_db
db_main = client.main_db

def merge_collection():
    result = db_batch.col_1_loc.find({}, {'_id' : False})
    #result = db_main.t_tourism_filter_2.find({}, {'_id' : False})
    print "Result found :: %d" % (result.count())
    pol_result = []
    for r in result:
        pol_result.append(r)
    #Change the Collection name
    col_res = db_main.tourism_geolocation.insert_many(pol_result)
    #col_res = db_main.t_tourism_filter.insert_many(pol_result)
    p_res = col_res.inserted_ids
    print "Total docs appended are %d" % (len(p_res))


if __name__ == "__main__":
    merge_collection()
    print "Collection passed to main_db!!"
