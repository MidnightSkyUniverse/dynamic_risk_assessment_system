"""
    Author: Ali Binkowska
    Date: Jan 2022
    Data ingestion - the script looks for 'csv' data and combine them into one pandas DF
"""
import pandas as pd
import os
import json
from sklearn.model_selection import train_test_split
from functions import db_select, db_insert

#import logging
#logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
#logger = logging.getLogger()


#############Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']
output_file = config['output_file']
test_data_path = config['test_data_path']
test_file = config['test_file']

#############Function for data ingestion
def merge_multiple_dataframe(hex_value):
    """
        Compile all datasets and store them in one csv file
    """
    #logging.info(f"Collect all csv files from {input_folder_path} and merge them")
    datasets = [x for x in os.listdir(input_folder_path) if x[-4:]=='.csv']
    combined = pd.DataFrame()
    for dataset in datasets:
        data = pd.read_csv(input_folder_path + dataset) 
        combined = combined.append(data)
        
    # Save combined 
    #logging.info(f"Save combined pandas dataframe to {output_folder_path} folder")
    result = combined.drop_duplicates()
    train, test = train_test_split(result, test_size=0.2, random_state=42, shuffle=True)
    train.to_csv(output_folder_path + output_file, index=False)
    test.to_csv(test_data_path + test_file, index=False)

    # Check which files are mentioned in the db
    files = db_select("SELECT file from ingested_files;")

    # Insert new filename to the database
    commands = []
    for dataset in datasets:
        commands.append(f"""
        INSERT INTO ingested_files (file,hex) values ('{dataset}', '{hex_value}')
        """
        )

    db_insert(commands)

