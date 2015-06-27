__author__ = 'Tang'

import json

data = json.load(open("disease.data"))

fields = ["Treatment", "Symptoms", "Prevention", "Causes"]
total_count = 0
count = {}

for item in fields:
    count[item] = 0

for disease_name in data:
    disease = data[disease_name]
    total_count += 1
    for item in fields:
        if item in disease:
            count[item] += 1

print("Total has {0}".format(total_count))
for item in fields:
    print("{0} has {1}".format(item, count[item]))


import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", # your host, usually localhost
                     user="root", # your username
                     passwd="", # your password
                     db="med") # name of the data

cur = db.cursor()

for disease_name in data:
    disease = data[disease_name]
    if "Treatment" in disease:
        treatment = disease["Treatment"]
    else:
        treatment = None
    if "Prevention" in disease:
        prevention = disease["Prevention"]
    else:
        prevention = None
    if "Causes" in disease:
        causes = disease["Causes"]
    else:
        causes = None
    print('INSERT INTO disease (causes) VALUES ("{0}")'.format(causes))
    cur.execute('INSERT INTO disease (causes) VALUES ("{0}")'.format(causes))