"""
    Author: Ali Binkowska
    Date: Jan 2022
"""
import ingestion
import training
import scoring
import deployment
import diagnostics
import reporting
import logging
import json
import os
import ast

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()


############# Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f)

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']
output_file = config['output_file']
ingested_files = config['ingested_files']
prod_deployment_path = config['prod_deployment_path']
score = config['scoring']
###### Step 1 
# check existance of new data. If positive, combine all datasets into one to re-train the model

# Combine list of .csv files with a list of files that contributed to the dataset
logging.info(f"Check for new data files in {input_folder_path}")
# Read list of ingested files
try:
    with open(ingested_files, 'rb') as f:
        lines = f.readlines()
except FileNotFoundError:
    logging.error(f"The file {ingested_files} cannot be found")
    lines = []

# Look for all csv fils in data folder
all_files = [x for x in os.listdir(input_folder_path) if x[-4:]=='.csv']
# Compare lists of ingested files and all csv files
for line_ in lines:
    if line_.decode('utf8').strip() in all_files:
        all_files.remove(line_.decode('utf8').strip())

# If there is new data, combine all csv-s and run train the model again
if len(all_files):
    logging.info(f"Files that have not been included in the dataset {all_files}")
    try:
        ingestion.merge_multiple_dataframe()
        logging.info("Executed ingestion() script to include new data")
    except:
        logging.error("Issue with ingestion() function")
else:
    logging.info(f"There are no new datasets in {input_folder_path}")


###### Step 2 
# If new data existis, re-train the model and check for model drift
#check whether the score from the deployed model is different from the score from the model that uses the newest ingested data
if len(all_files): #New data exists -> we proceed with re-training
    logging.error("Use production model to do predictions on new dataset")
    predictions = diagnostics.model_predictions(output_folder_path + '/' + output_file)
    new_f1 = scoring.score_model() 
    logging.error(f"New F1 score is {new_f1}")
    
    # Read the last score 
    with open(prod_deployment_path + '/' + score, 'r') as f:
        old_f1 = ast.literal_eval(f.read().strip())     
    logging.error(f"Previous F1 score is {old_f1['score']}")

    if new_f1 < old_f1:
        print("Model drifts")

##################Deciding whether to proceed, part 2
#if you found model drift, you should proceed. otherwise, do end the process here



##################Re-deployment
#if you found evidence for model drift, re-run the deployment.py script

##################Diagnostics and reporting
#run diagnostics.py and reporting.py for the re-deployed model







