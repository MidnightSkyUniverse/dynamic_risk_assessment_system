"""
    Author: Ali Binkowska
    Date: Jan 2022

"""
import pandas as pd
import timeit
import os
import json
import pickle
import logging 
from functions import process_data, execute_command

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

##################Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
output_file = config['output_file']
# test data
test_data_path = os.path.join(config['test_data_path']) 
test_file = config['test_file']
# model
#output_model_path = os.path.join(config['output_model_path'])
prod_deployment_path = config['prod_deployment_path']
output_model = config['output_model']
# numeric columns
numeric_cols = config['numeric_cols']


##################Function to get model predictions
def model_predictions(file_name):
    """
        Output: predictions
    """ 
#    logging.info(f"Load model from {output_model}")
    with open(prod_deployment_path + output_model, 'rb') as f:
        model = pickle.load(f)

#    logging.info(f"Load test data from {test_file} and splitting into X and Y")
    X, y = process_data(file_name)

#    logging.info("Model predicting")
    predicted = model.predict(X)

    return predicted 

##################Function to get summary statistics
def dataframe_summary():
    """
    Statistics:  means, medians, and standard deviations
    """
    logging.info(f"Calculate the statistics for the dataset")
    thedata = pd.read_csv(dataset_csv_path + output_file)

    mean = thedata.mean(axis=0)
    median = thedata.median(axis=0)
    std = thedata.std(axis=0)
    results = []
    for col in numeric_cols:
        logging.info(f"Statistics for  for {col}")
        mean_ = mean[col]
        median_ = median[col]
        std_ = std[col]
        logging.info(f"mean: {mean_} - median: {median_} - std: {std_}")
        results.append({
                "feature": col, 
                'mean': mean_,
                'median': median_,
                'std': std_
        })
        
    return results

def missing_data():
    """
    Statistics on NA data
    """
    logging.info(f"Calculate the statistics for the dataset")
    thedata = pd.read_csv(dataset_csv_path + output_file)

    na = thedata.isna().sum()
    
    results = [na[i]/len(thedata.index) for i in range(len(na))]
    return results

##################Function to get timings
def execution_time():
    starttime = timeit.default_timer()
    os.system("python training.py")
    timing1=timeit.default_timer() - starttime
    
    starttime = timeit.default_timer()
    os.system("python ingestion.py")
    timing2=timeit.default_timer() - starttime
    
    logging.info(f"Time to execute training.py: {timing1}")
    logging.info(f"Time to execute ingestion.py: {timing2}")

    return (timing1, timing2)

##################Function to check dependencies
def outdated_packages_list():
    """
    Use requirements.txt to list current and latest version of required packages
    """
    logging.info("Prepare list of outdated packages with target version")
    # collect the command output
    pip_outdated = execute_command(["pip", "list", "--outdated"])

    # read current requirements file
    with open("requirements.txt", 'rb') as f:
        lines = [x.decode('utf8').strip() for x in f.readlines()]

    results = []
    for l in lines:
        x = l.split("==")
        for y in pip_outdated:
            if x[0] == y[0]:
                results.append(f"{y[0]} - {y[1]} - {y[2]}")
    
    return results


#if __name__ == '__main__':
#    model_predictions()
#    dataframe_summary()
#    missing_data()
#    execution_time()
#    outdated_packages_list()





    
