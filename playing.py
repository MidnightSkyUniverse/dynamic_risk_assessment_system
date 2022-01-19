import datetime
from functions import random_hex, db_select, db_insert
import os
import json

hex_value = random_hex()
created = datetime.datetime.now()

with open('config.json','r') as f:
    config = json.load(f)

input_folder_path = config['input_folder_path']


#print(f"created: {created}")
#command = f"""INSERT INTO ingested_files (file,hex,created) 
#                values ('dataset2.csv', '{hex_value}','{created}');"""
#db_insert([command])

datasets = [x for x in os.listdir(input_folder_path) if x[-4:]=='.csv']

result = db_select("SELECT file from ingested_files;")
#ingested = [x[0] for x in result]
#print (ingested)

for x in result:
    datasets.append(x[0])

print(list(set(datasets)))

#combined = list(set(result + ingested))
#print(combined)
