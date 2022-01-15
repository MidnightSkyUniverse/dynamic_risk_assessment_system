"""
"""
import os
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

##################Load config.json and correct path variable
with open('config.json','r') as f:
    config = json.load(f) 

#dataset_csv_path = os.path.join(config['output_folder_path']) 
prod_deployment_path = os.path.join(config['prod_deployment_path']) 

# model
output_model_path = config['output_model_path']
model_path = config['output_model']
scoring = config['scoring']
ingested_file = config['ingested_files']

####################function for deployment
def store_model_into_pickle():#model):
    #copy the latest pickle file, the latestscore.txt value, and the ingestfiles.txt file into the deployment directory
       
    logging.info(f"Copy model to production folder {prod_deployment_path}") 
    os.system(f"cp {output_model_path}/{model_path} {prod_deployment_path}")
        
    logging.info(f"Copy model scoring to  folder {prod_deployment_path}") 
    os.system(f"cp {output_model_path}/{scoring} {prod_deployment_path}")
    
    logging.info(f"Copy list of ingested files to  folder {prod_deployment_path}") 
    os.system(f"cp {ingested_file} {prod_deployment_path}")
  

  
store_model_into_pickle()
