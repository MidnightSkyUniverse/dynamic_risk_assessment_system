"""
"""
import os
import json

#import logging
#logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
#logger = logging.getLogger()

##################Load config.json and correct path variable
with open('config.json','r') as f:
    config = json.load(f) 

prod_deployment_path = os.path.join(config['prod_deployment_path']) 
# model
output_model_path = config['output_model_path']
model_path = config['output_model']


def store_model_into_pickle(hex_value):
       
    #logging.info(f"Copy model to production folder {prod_deployment_path}") 
    os.system(f"cp {output_model_path}/{model_path} {prod_deployment_path}")
        
    #logging.info(f"Set model scoring as PRODUCTION in the db") 
    set_f1_as_production(hex_value)
