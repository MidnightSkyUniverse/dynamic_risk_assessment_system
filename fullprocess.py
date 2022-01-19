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
import timeit
sys.path.append(os.getcwd())

import ingestion
import training
import scoring
import deployment
import diagnostics
import reporting
import functions
from functions import random_hex, db_select, db_insert

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()


############# Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f)

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']
output_file = config['output_file']
prod_deployment_path = config['prod_deployment_path']
# test data
test_data_path = os.path.join(config['test_data_path'])
test_file = config['test_file']

# This value will be used to recognize the data inserted in one session
hex_value = random_hex()

# ************************* Step 1 ************************* 
# check existance of new data. If positive, combine all 
# datasets into one and use it to test the model
# ********************************************************** 

# Look for all csv fils in the data folder and all files stored in the db
local_csv = [x for x in os.listdir(input_folder_path) if x[-4:]=='.csv']
stored_csv = [x[0].strip() for x in db_select("SELECT file from ingested_files;")]
new_csv = list(set(local_csv) - set(stored_csv))

# If there is new data, combine all csv-s and run train the model again
if len(new_csv):
    logging.info(f"Step 1: New datasets were found:  {new_csv}")
    try:
        # Meassure timing of the script
        starttime = timeit.default_timer()
        ingestion.merge_multiple_dataframe(hex_value)
        timing=timeit.default_timer() - starttime
        execution_time('ingestion.py',timing,hex_value)
        logging.info("Step 1: Executed ingestion() script successfully")
    except:
        logging.error("Step 1: Issue with ingestion() script")
else:
    logging.info(f"Step 1: There are no new datasets in {input_folder_path}")
    # We can finish the script here
    exit()

# ************************* Step 2 ************************* 
# If new data existis, use combined data to do predictions
# and scsoring (F1). Old and new scores are compared.
# ********************************************************** 

logging.error("Step 2: Use production model to do predictions on new dataset")
predictions = diagnostics.model_predictions(output_folder_path + output_file)
new_f1 = scoring.score_model(output_folder_path + output_file,'istest') 
logging.error(f"Step 2: New F1 score is {new_f1}")
    
# Read the PRODUCTION score
command = 'select f1_score from f1 WHERE is_production=True' 
old_f1 = db_select(command)[0][0]
logging.error(f"Previous F1 score is {old_f1}")

if not new_f1:# >= float(old_f1['score']): 
    logging.info("Model is not drifting => exit()")
    # Once there is no model drift, we can complete the script here
    exit()


# ************************* Step 3 ************************* 
# Model re-training & scoring. Copy new model, scores and
# list of ingested files to production folder
# ********************************************************** 
logging.info("Training the model on the new dataset")
starttime = timeit.default_timer()
training.train_model()
timing=timeit.default_timer() - starttime
execution_time('training.py',timing,hex_value)


predictions = diagnostics.model_predictions(output_folder_path + output_file)
new_f1 = scoring.score_model(test_data_path + test_file, hex_value) 
logging.error(f"New F1 score is {new_f1}")
 
logging.info(f"Copy model to {prod_deployment_path}, set F1 score as PRODUCTION")
deployment.store_model_into_pickle(hex_value)

# ************************* Step 4 ************************* 
# Run reporting which will create and save confusion matrix
# Execute apicalls.py for diagnostics
# ********************************************************** 
try:
    reporting.cf_matrix(test_data_path + test_file)
    logging.info("Confusion matrix has been created")
except:
    logging.error("Issue with confusion matrix creation (reporting.py script)")

try:
    diagnostics.dataframe_summary(hex_value) 
    diagnostics.missing_data()
    logging.info("Diagnostics have been executed for missing data and feature stats")
except:
    logging.error("Issue with running diagnostics")


try:
    results = functions.execute_command(['python','apicalls.py'])
    logging.info(f"API calls executed successfully {results}")
except:
    logging.error("Issue with apicalls.py")







