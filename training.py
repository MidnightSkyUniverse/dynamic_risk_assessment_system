"""
    Author: Ali Binkowska
    Date: Jan 2022

    
"""
import pickle
import os
from sklearn.linear_model import LogisticRegression
import json
import logging
from functions import process_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

# Define paths 
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
output_file = config['output_file']
# model
model_path = os.path.join(config['output_model_path']) 
output_model =  config["output_model"]


def train_model():
    """
    Process the data and train the model based on Logistic Regression algorithm
    The model is saved after the training
    """    

    # Define this logistic regression model for training
#    logging.info("Define Logistic Regression model")
    logit = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                    intercept_scaling=1, l1_ratio=None, max_iter=100,
                    #multi_class='warn', n_jobs=None, penalty='l2',
                    multi_class='auto', n_jobs=None, penalty='l2',
                    random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                    warm_start=False)
    
    # Fit the logistic regression to your data
#    logging.info("Transform the data from pandas into X and y")
    X, y = process_data(dataset_csv_path + '/' + output_file) 
    #print (X)
    #print(y)

    # Train the model 
#    logging.info("Train the model on the data")
    model = logit.fit(X,y)
    
    #write the trained model to your workspace in a file called trainedmodel.pkl
#    logging.info(f"Save the model to file {output_model}")
    pickle.dump(model, open(model_path + '/' +  output_model, 'wb'))    


