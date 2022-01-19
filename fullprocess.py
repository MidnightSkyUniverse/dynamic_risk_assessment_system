"""
    Author: Ali Binkowska
    Date: Jan 2022

    The script 
"""
import sys
import os
import logging
import json
import ast
sys.path.append(os.getcwd())

import ingestion
import training
import scoring
import deployment
import diagnostics
import reporting
import functions
from functions import random_hex, db_select, db_insert

logging.basicConfig(filename='fullprocess.log', level=logging.INFO, format="%(asctime)s - %(message)s")
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
# test data
test_data_path = os.path.join(config['test_data_path'])
test_file = config['test_file']

# This value will be used to recognize the data inserted in one session
hex_value = random_hex()

# ************************* Step 1 ************************* 
# check existance of new data. If positive, combine all 
# datasets into one and use it to test the model
# ********************************************************** 

# Look for all csv fils in the data folder
csv_files = [x for x in os.listdir(input_folder_path) if x[-4:]=='.csv']

# Check the db for previously ingested

try:
    with open(prod_deployment_path + ingested_files, 'rb') as f:
        lines = f.readlines()
except FileNotFoundError:
    logging.error(f"The file {ingested_files} cannot be found")
    lines = []

# Compare lists of ingested files and all csv files
for line_ in lines:
    if line_.decode('utf8').strip() in csv_files:
        csv_files.remove(line_.decode('utf8').strip())

# If there is new data, combine all csv-s and run train the model again
if len(csv_files):
    logging.info(f"Files that have not been included in the dataset {csv_files}")
    try:
        ingestion.merge_multiple_dataframe()
        logging.info("Executed ingestion() script to include new data")
    except:
        logging.error("Issue with ingestion() function")
else:
    logging.info(f"There are no new datasets in {input_folder_path}")
    # We can finish the script here
    exit()

# ************************* Step 2 ************************* 
# If new data existis, use combined data to do predictions
# and scsoring (F1). Old and new scores are compared.
# ********************************************************** 

logging.error("Use production model to do predictions on new dataset")
predictions = diagnostics.model_predictions(output_folder_path + output_file)
new_f1 = scoring.score_model(output_folder_path + output_file) 
logging.error(f"New F1 score is {new_f1}")
    
# Read the last score 
with open(prod_deployment_path + score, 'r') as f:
    old_f1 = ast.literal_eval(f.read().strip())     
logging.error(f"Previous F1 score is {old_f1['score']}")

if new_f1:# >= float(old_f1['score']): 
    logging.info("Model is not drifting, so we can conclude the progam")
    # Once there is no model drift, we can complete the script here
    exit()


# ************************* Step 3 ************************* 
# Model re-training & scoring. Copy new model, scores and
# list of ingested files to production folder
# ********************************************************** 
logging.info("Training of the model on the new dataset")
training.train_model()

predictions = diagnostics.model_predictions(output_folder_path + output_file)
new_f1 = scoring.score_model(test_data_path + test_file) 
logging.error(f"New F1 score is {new_f1}")
 
logging.info(f"Copy model, scores and list of ingested files to {prod_deployment_path}")
deployment.store_model_into_pickle()

# ************************* Step 4 ************************* 
# Run reporting which will create and save confusion matrix
# Execute apicalls.py for diagnostics
# ********************************************************** 
reporting.score_model(test_data_path + test_file)
try:
    logging.info("Confusion matrix has been created")
except:
    logging.error("Issue with confusion matrix creation (reporting.py script)")

results = functions.execute_command(['python','apicalls.py'])
try:
    logging.info(f"API calls executed successfully {results}")
except:
    logging.error("Issue with apicalls.py")







