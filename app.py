"""
    Author: Ali Binkowska
    Date: Jan 2022
"""
from flask import Flask, request, render_template
import json
import os
import subprocess


# Save the link to Heroku database, the link can change between session
try:
    DATABASE_URL = os.environ['DATABASE_URL']
except:
    DATABASE_URL = subprocess.check_output(['heroku', 'config:get', 'DATABASE_URL', '-a', 'risk-assess-sys']).decode('utf8').strip()


# Those can be imported only once we have saved DB URL
import diagnostics
import scoring
from functions import db_select


######################Set up variables for use in our script
app = Flask(__name__)
#app.secret_key = config['SECRET_KEY']

with open('config.json','r') as f:
    config = json.load(f) 
dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = config['test_data_path']
output_model_path = config['output_model_path']
output_model = config['output_model']
apireturns = config['apireturns']

prediction_model = None
hex_production = db_select("select hex from f1 where is_production=True")[0][0]

# ***************** Prediction Endpoint ************************
@app.route('/',methods=['GET','OPTIONS'])
def root():
   render_template('index.html',data="Hey there!") 

# ***************** Prediction Endpoint ************************
@app.route("/prediction", methods=['POST','OPTIONS'])
def predict():        
    #file_name = json.loads(request.data)
#
    request_data = request.get_json()
    file_name = request_data['file_name']
    predictions = diagnostics.model_predictions(file_name)
    return  {"data": predictions.tolist()}


# ***************** Scoring Endpoint ************************
@app.route("/scoring", methods=['GET','OPTIONS'])
def stats1():        
    f1_score = db_select("select f1_score from f1 where is_production=True")[0][0]
    return {"data": f1_score}

# ***************** Summary on the datasets Endpoint ************************
@app.route("/summarystats", methods=['GET','OPTIONS'])
def stats2():        
    command = f"select feature, mean,median,std from feature_stats where hex = '{hex_production}'"
    data = db_select(command)
    return {"data": data}

# ***************** Diagnostics Endpoint ************************
@app.route("/diagnostics", methods=['GET','OPTIONS'])
def stats3():        
    command1 = f"select feature, percentage from missing_data where hex = '{hex_production}'"
    command2 = f"select file,timing from script_timing where hex = '{hex_production}'"
    x = db_select(command1) 
    y = db_select(command2) 
    z = diagnostics.outdated_packages_list()
    
    data = {
        "missing_data": x,
        "execution_time": y,
        "outdated_packages": z
    }

    return data

# ***************** Endpoint returning name of txt file to save output  ************************
@app.route("/apireturns",methods=['GET'])
def name():
    return output_model_path + apireturns

#if __name__ == "__main__":    
#    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
