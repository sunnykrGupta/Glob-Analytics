# coding: utf-8


from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)
db_main = client.main_db
db_batch = client.batch_db

def process_db():
    result = db_main.t_tourism_filter_2.find({},{ '_id' : False })
    #result = db_batch.col_2.find({},{ '_id' : False })
    print "Total record fetched %d" % (result.count())

    col_1 = []
    col_2 = []
    col_3 = []
    col_4 = []
    col_5 = []
    col_6 = []
    col_7 = []
    cnt = 0
    for r in result:
        cnt += 1
        if(cnt <= 10000):
            col_1.append(r)
        '''
        elif(cnt > 10000 and cnt <= 22000):
            col_2.append(r)
        elif(cnt > 20000 and cnt <= 30000):
            col_3.append(r)
        elif(cnt > 7350 and cnt <= 9800):
            col_4.append(r)
        elif(cnt > 9800 and cnt <= 12250):
            col_5.append(r)
        elif(cnt > 12250 and cnt <= 14700):
            col_6.append(r)
        elif(cnt > 14700):
            col_7.append(r)
        '''
    #insert the batch into diff. collections
    db_batch.col_1.insert_many(col_1)
    print "Insertion Done into col_1!!"
    '''
    db_batch.col_2.insert_many(col_2)
    print "Insertion Done into col_2!!"
    db_batch.col_3.insert_many(col_3)
    print "Insertion Done into col_3!!"
    db_batch.col_4.insert_many(col_4)
    print "Insertion Done into col_4"
    db_batch.col_5.insert_many(col_5)
    print "Insertion Done into col_5"
    db_batch.col_6.insert_many(col_6)
    print "Insertion Done into col_6"
    db_batch.col_7.insert_many(col_7)
    print "Insertion Done into col_7"
    '''

if __name__ == "__main__":
    process_db()
    print "Processing Done!!"


