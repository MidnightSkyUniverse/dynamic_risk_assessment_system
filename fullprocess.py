"""
    Author: Ali Binkowska
    Date: Jan 2022

    The script 
"""
import sys
import os
import subprocess
import logging
import json
import ast
import timeit
sys.path.append(os.getcwd())

# Save the link to Heroku database, the link can change between session
try:
    DATABASE_URL = os.environ['DATABASE_URL']
except:
    DATABASE_URL = subprocess.check_output(['heroku', 'config:get', 'DATABASE_URL', '-a', 'risk-assess-sys']).decode('utf8').strip()

# Import of script will take place once database link is defined
import ingestion
import training
import scoring
import deployment
import diagnostics
import reporting
import functions
from functions import random_hex, db_select, db_insert
from reporting import  draw_f1,  draw_timing, draw_stats_on_features


# ************************* Step 0 ************************* 
# Set logging 
# Import variables from config.json
# Set hex_value which will be unique for each run 
# ********************************************************** 
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

with open('config.json','r') as f:
    config = json.load(f)

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']
output_file = config['output_file']
prod_deployment_path = config['prod_deployment_path']
test_data_path = os.path.join(config['test_data_path'])
test_file = config['test_file']

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
        diagnostics.execution_time('ingestion.py',timing,hex_value)
        logging.info("Step 1: Executed ingestion() script successfully")
    except Exception as e:
        logging.error("Error: Issue with ingestion() script")
        logging.error(f"Error: {e}")
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
try:
    old_f1 = db_select(command)[0][0]
    logging.info(f"Step 2: Previous F1 score is {old_f1}")
except:
    old_f1 = 0
    logging.error(f"Error: F1 score set to 0")

if not new_f1:# >= float(old_f1['score']): 
    logging.info("Step 2: Model is not drifting => exit()")
    # Once there is no model drift, we can complete the script here
    exit()


# ************************* Step 3 ************************* 
# Model re-training & scoring. Copy new model, scores and
# list of ingested files to production folder
# ********************************************************** 
logging.info("Step 3: Training the model on the new dataset")
starttime = timeit.default_timer()
training.train_model()
timing=timeit.default_timer() - starttime
diagnostics.execution_time('training.py',timing,hex_value)


predictions = diagnostics.model_predictions(output_folder_path + output_file)
new_f1 = scoring.score_model(test_data_path + test_file, hex_value) 
logging.error(f"Step 3: New F1 score is {new_f1}")
 
logging.info(f"Step 4: Copy model to {prod_deployment_path}, set F1 score as PRODUCTION")
deployment.store_model_into_pickle(hex_value)


# ************************* Step 4 ************************* 
# Run reporting which will create and save confusion matrix
# Execute apicalls.py for diagnostics
# ********************************************************** 
try:
    reporting.cf_matrix(test_data_path + test_file)
    logging.info("Step 4: Confusion matrix has been created")
except:
    logging.error("Error: Issue with confusion matrix creation (reporting.py script)")

try:
    diagnostics.dataframe_summary(hex_value) 
    diagnostics.missing_data(hex_value)
    logging.info("Step 4: Diagnostics have been executed for missing data and feature stats")
except Exception as e:
    logging.error("Error: Issue with running diagnostics")
    logging.error(f"Error: {e}")

try:
    draw_f1()
    draw_stats_on_features()
    draw_timing()
    logging.info("Step 4: Charts have been generated")
except Exception as e:
    logging.error("Error: Issue with running generating charts")
    logging.error(f"{e}")

"""
try:
    results = functions.execute_command(['python','apicalls.py'])
    logging.info(f"Step 4: API calls executed successfully {results}")
except:
    logging.error("Error: Issue with apicalls.py")
"""






