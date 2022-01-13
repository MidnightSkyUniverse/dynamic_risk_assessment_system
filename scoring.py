"""
    Author: Ali Binkowska
    Date: Jan 2022

    Scoring of the model
"""
from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression
import json
import logging
from functions import process_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

#################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

test_data_path = os.path.join(config['test_data_path']) 
test_file = config['test_file'] 
# model
output_model_path = os.path.join(config['output_model_path'])
output_model = config['output_model']
# scoring
scoring = config['scoring']


#################Function for model scoring
def score_model():
    #this function should take a trained model, load test data, and calculate an F1 score for the model relative to the test data
    #it should write the result to the latestscore.txt file
    logging.info(f"Load model from {output_model}")
    with open(output_model_path + '/' + output_model, 'rb') as f:
        model = pickle.load(f)

    logging.info(f"Load test data from {test_file} and splitting into X and Y")
    X, y = process_data(test_data_path + '/' + test_file)    

    logging.info("Model scoring with F1")
    predicted = model.predict(X)

    f1score=metrics.f1_score(predicted,y)
    logging.info(f"F1 score: {f1score}")

    with open(output_model_path + '/' + scoring, 'a') as f:
        entry = {'metric': 'f1', 'score': f1score}
        f.write(str(entry)+'\n')

    

score_model()
