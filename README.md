## Dynamic Risk Assessment System
Udacity nanodegree program


![model experiment with metrics](/screenshots/dvc_exp_show.png)

### Built With
Technologies used in the project
* [GitHub](github.com)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* crontab


### Getting Started

#### Conda environment
This project was setup using miniconda. To setup the enviornment run:
```conda env create -f environment.yml```

#### Project execution
The project files can be executed separately. Each scripts has logging commented out.
In case of need to troubleshoot, the logging can be enabled.

To execute the project as a whole, execute ```python fullprocess.py```
This is the logic behind the script:

1. We check whether there are new datasets and if yes, we combine all data in one dataset with ingestion.py
	Otherwise we end the program

2. Run predictions of the production model on new dataset with diagnostics.py -> model_predictions

3. We score the predictions with scoring.py -> score_model and compare new F1 with one saved

3. If new F1 score is lower, we have a model drift and so we go with step 4. Otherwise we end the program

4. Retrain the model on new dataset with training.py -> train_model()  

5. Run diagnostics.py -> model_predictions() to get new model predictions 

6. Score model with scoring.py -> score_model. That will save new F1 to the file

7. Run deployment.py to save new model. scores and lsit of ingested files to production folder


#### Continuous diagnostics

There is a script called `execute_fullprocess.sh` which can be configured as cron job
and execute fullprocess.py in regular intervals.

#### Model documentation


#### Model execution


### Model metrics

### Model tests

### GitHub workflow config
### Contact
Project Link: https://github.com/MidnightSkyUniverse/dynamic_risk_assessment_system

## For Udacity Team

