
import json
import csv
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
'''
 database ::
'''
db_batch = client.batch_db

def write_csv():
    #tell computer where to put CSV
    outfile_path = "glob_geo_religion_density.csv"
    writer = csv.writer(open(outfile_path, 'wb'))

    #create a list with headings for our columns
    headers = ['iso2c', 'country', 'all', 'lat', 'lng']
     #write the row of headings to our CSV file
    writer.writerow(headers)

    results = db_batch.religion_final.find({}, {'_id' : False})

    for record in results:
        for (country, values) in record.iteritems():
            #run through each item in results, and jump to an item in that dictionary
            print country, " ",
            row = []
            #add every 'cell' to the row list, identifying the item just like an index in a list
            row.append(str(values["iso2c"].encode('utf-8')))
            row.append(str(country.encode('utf-8')))
            row.append(values["all"])
            row.append(values["lat"])
            row.append(values["lng"])
            #once you have all the cells in there, write the row to your csv
            writer.writerow(row)
    print "CSV Records Inserted!!"

if __name__ == "__main__":
    write_csv()
    print "CSV File Created!!"
