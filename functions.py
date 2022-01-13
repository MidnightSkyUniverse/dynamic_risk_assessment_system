"""
    Author: Ali Binkowska
    Date: Jan 2022

    Collection of functions used through the pipeline
"""
import pandas as pd
import json

with open('config.json','r') as f:
    config = json.load(f) 

label = config['label']
X_cols = config['X_cols']


def process_data(file_path):
    """
    Read cvs file and split the dataset into X and y
    """
    trainingdata = pd.read_csv(file_path) #pd.read_csv(dataset_csv_path + '/' + output_file)
    X=trainingdata.loc[:,X_cols].values.reshape(-1, len(X_cols))
    y=trainingdata[label].values.reshape(-1, 1).ravel()
    
    return (X,y) 



