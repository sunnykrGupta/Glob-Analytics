# coding: utf-8


from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)
db_main = client.main_db
db_batch = client.batch_db

def process_db():
    result = db_main.politic_filtr_2.find({},{ '_id' : False })
    print "Total record fetched %d" % (result.count())

    pol_1 = []
    pol_2 = []
    pol_3 = []
    pol_4 = []
    pol_5 = []
    pol_6 = []
    pol_7 = []
    cnt = 0
    for r in result:
        cnt += 1
        if(cnt <= 2450):
            pol_1.append(r)
        elif(cnt > 2450 and cnt <= 4900):
            pol_2.append(r)
        elif(cnt > 4900 and cnt <= 7350):
            pol_3.append(r)
        elif(cnt > 7350 and cnt <= 9800):
            pol_4.append(r)
        elif(cnt > 9800 and cnt <= 12250):
            pol_5.append(r)
        elif(cnt > 12250 and cnt <= 14700):
            pol_6.append(r)
        elif(cnt > 14700):
            pol_7.append(r)
    #insert the batch into diff. collections
    db_batch.pol_1.insert_many(pol_1)
    print "Insertion Done into Pol_1!!"
    db_batch.pol_2.insert_many(pol_2)
    print "Insertion Done into Pol_2!!"
    db_batch.pol_3.insert_many(pol_3)
    print "Insertion Done into Pol_3!!"
    db_batch.pol_4.insert_many(pol_4)
    print "Insertion Done into Pol_4"
    '''
    db_batch.pol_5.insert_many(pol_5)
    print "Insertion Done into Pol_5"
    db_batch.pol_6.insert_many(pol_6)
    print "Insertion Done into Pol_6"
    db_batch.pol_7.insert_many(pol_7)
    print "Insertion Done into Pol_7"
    '''

if __name__ == "__main__":
    process_db()
    print "Processing Done!!"


