"""
    Author: Ali Binkowska
    Date: Jan 2022

    Scoring of the model
"""
import pickle
import os
from sklearn import metrics
import json
#import logging
from functions import process_data, db_insert

#logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
#logger = logging.getLogger()

#################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

test_data_path = os.path.join(config['test_data_path']) 
test_file = config['test_file'] 
# model
output_model_path = os.path.join(config['output_model_path'])
output_model = config['output_model']
prod_deployment_path = config['prod_deployment_path']
# scoring
#scoring = config['scoring']


#################Function for model scoring
def score_model(file_path,hex_value):
    #this function should take a trained model, load test data, and calculate an F1 score for the model relative to the test data
    #it should write the result to the latestscore.txt file
#    logging.info(f"Load model from {output_model}")
    with open(prod_deployment_path + output_model, 'rb') as f:
        model = pickle.load(f)

#    logging.info(f"Load test data from {test_file} and splitting into X and Y")
    X, y = process_data(file_path)    

#    logging.info("Model predicting and scoring with F1")
    predicted = model.predict(X)

    f1_score=metrics.f1_score(predicted,y)
#    logging.info(f"F1 score: {f1score}")

#    with open(output_model_path + scoring, 'w') as f:
#        entry = {'metric': 'f1', 'score': f1score}
#        f.write(str(entry)+'\n')
    
    command = f"INSERT INTO f1 (f1_score,hex) values ('{f1_score}', '{hex_value}');"
    db_insert([command])

    return f1_score    

