"""
    Author: Ali Binkowska
    Date: Jan 2022

    Collection of functions used through the pipeline
"""
import pandas as pd
import json
import subprocess

with open('config.json','r') as f:
    config = json.load(f) 

label = config['label']
numeric_cols = config['numeric_cols']


def process_data(file_path):
    """
    Read cvs file and split the dataset into X and y
    """
    trainingdata = pd.read_csv(file_path) 
    X=trainingdata.loc[:,numeric_cols].values.reshape(-1, len(numeric_cols))
    y=trainingdata[label].values.reshape(-1, 1).ravel()
    
    return (X,y) 

def execute_command(cmd_list):
    """
    Function execute command and returns stdout as a list
    
    input: command as a list ex ['pip','list','--outdated']
    """
    process = subprocess.Popen(cmd_list, stdout = subprocess.PIPE)
    results = []
    while True:
        output = process.stdout.readline()
        if output.decode('utf8') == '' and process.poll() is not None:
            break
        if output:
            results.append(output.decode('utf8').strip().split())
    rc = process.poll()

    return results

