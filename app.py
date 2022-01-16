"""
    Author: Ali Binkowska
    Date: Jan 2022
"""
from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import diagnostics
import json
import os
from scoring import score_model


######################Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = config['test_data_path']
output_model_path = config['output_model_path']
output_model = config['output_model']
prediction_model = None


#######################Prediction Endpoint
@app.route("/prediction", methods=['POST','OPTIONS'])
def predict():        
    #file_name = json.loads(request.data)
#
    request_data = request.get_json()
    file_name = request_data['file_name']
    predictions = diagnostics.model_predictions(file_name)
    return  {"data": predictions.tolist()}


#######################Scoring Endpoint
@app.route("/scoring", methods=['GET','OPTIONS'])
def stats1():        
    response = score_model()
    return {"data": response}

#######################Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET','OPTIONS'])
def stats2():        
    #check means, medians, and modes for each column
    results =  diagnostics.dataframe_summary()
    return {"data": results}

#######################Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET','OPTIONS'])
def stats3():        
    x = diagnostics.missing_data()
    y = diagnostics.execution_time()
    z = diagnostics.outdated_packages_list()
    
    data = {
        "missing_data": x,
        "execution_time": y,
        "outdated_packages": z
    }

    return data

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
