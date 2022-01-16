# dynamic_risk_assessment_system
Dynamic Risk Assessment System
Udacity nanodegree program



fullprocess.py
1. We check whether there are new datasets and if yes, we combine all data in one dataset with ingestion.py
	Otherwise we end the program

2. Run predictions of the production model on new dataset with diagnostics.py -> model_predictions

3. We score the predictions with scoring.py -> score_model and compare new F1 with one saved

3. If new F1 score is lower, we have a model drift and so we go with step 4. Otherwise we end the program

4. Retrain the model on new dataset with training.py -> train_model()  

5. Run diagnostics.py -> model_predictions() to get new model predictions 

6. Score model with scoring.py -> score_model. That will save new F1 to the file

7. Run deployment.py to save new model. scores and lsit of ingested files to production folder

8. 
