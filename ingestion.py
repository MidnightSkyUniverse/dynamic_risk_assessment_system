"""
    Author: Ali Binkowska
    Date: Jan 2022
    Data ingestion - the script looks for 'csv' data and combine them into one pandas DF
"""
import pandas as pd
import os
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()


#############Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']
output_file = config['output_file']
ingested_files = config['ingested_files']



#############Function for data ingestion
def merge_multiple_dataframe():
    #check for datasets, compile them together, and write to an output file
#    logging.info(f"Collect all csv files from {input_folder_path} and merge them")
    datasets = [x for x in os.listdir(input_folder_path) if x[-4:]=='.csv']
    combined = pd.DataFrame()
    for dataset in datasets:
        data = pd.read_csv(input_folder_path + '/' + dataset) 
        combined = combined.append(data)
        
    # Save combined 
#    logging.info(f"Save combined pandas dataframe to {output_folder_path} folder")
    result = combined.drop_duplicates()
    result.to_csv(output_folder_path + '/' + output_file, index=False)

    # Save names of dataset files that were source of the data
#    logging.info(f"Save names of csv-s to {ingested_files}")
    with open(ingested_files, 'w') as f:
        for dataset in datasets:
            f.write(dataset+'\n')



if __name__ == '__main__':
    merge_multiple_dataframe()
