from functions import random_hex, db_select, db_insert
import os
import json

hex_value = random_hex()

with open('config.json','r') as f:
    config = json.load(f)

input_folder_path = config['input_folder_path']

# ***************** Ingestion **********************
#print(f"created: {created}")
#command = f"""INSERT INTO ingested_files (file,hex,created) 
#                values ('dataset2.csv', '{hex_value}','{created}');"""
#db_insert([command])
"""
datasets = [x for x in os.listdir(input_folder_path) if x[-4:]=='.csv']
stored = [x[0].strip() for x in db_select("SELECT file from ingested_files;")]
new_datasets = list(set(datasets) - set(stored))

commands=[]
for dataset in new_datasets:
    command = f"""INSERT INTO ingested_files (file,hex) 
                values ('{dataset}', '{hex_value}');"""
    commands.append(command)
db_insert(commands)

answer = db_select("select * from ingested_files")
#print(answer)

#******************** 
# Scoring
f1_score=0.60001222222222
command = f"INSERT INTO f1 (f1_score,hex,is_production) values ('{f1_score}', '{hex_value}','False');"
db_insert([command])

f1_score=0.000336498345
command = f"INSERT INTO f1 (f1_score,hex) values ('{f1_score}', '{hex_value}');"
db_insert([command])

f1_score=0.7111111190540809
command = f"INSERT INTO f1 (f1_score,hex) values ('{f1_score}', '{hex_value}');"
db_insert([command])

command = 'select f1_score from f1 WHERE is_production=True'
old_f1 = db_select(command)[0][0]
print(f"old score: {old_f1}")
"""

##########################

print(db_select("select hex from f1 where is_production=True")[0])
