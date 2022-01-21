## Dynamic Risk Assessment System
With an assumption that we have a Machine Learning model in production, the project
aims to check in regular intervals (per crontab configuration) for new datasets
and acts upon any new data that is saved. 
The model is tested for checking whether model drift, re-train if needed 
and new reporting of the model performance, data quality and timing of execution 
is saved to the database.

This project us par of Udacity nanodegree program.


![model experiment with metrics](/screenshots/dvc_exp_show.png)

### Built With
Technologies used in the project
* [GitHub](github.com)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Heroku](https://heroku.com)
* [PostreSQL on Heroku](https://www.postgresql.org/)
* [crontab](https://man7.org/linux/man-pages/man5/crontab.5.html)
* [reportlab for PDF generation](https://www.reportlab.com/docs/reportlab-userguide.pdf) 


### Getting Started

#### Conda environment
This project was setup using miniconda. To setup the enviornment run:
```conda env create -f conda_local.env```

#### Heroku with PostgreSQL
The project saves the data to Heroku database. So it is required to setup remote 
database and update DATABASE_URL to point to the database.

Script `dbsetup.py` creates tables in the database so it's first one to be executed before
we move to running next steps.
SCript `drop_tables.py` is used to drop all the tables so `dbsetup.py` can be re-run.

#### Project execution

The main script doing the job is `fullprocess.py`

The project files can be executed separately. Each script has logging system that can be used 
for troubleshooting. `fullprocess` is going through the scripts and depending on the conditions,
execute all or some of them every time new dataset is being saved to the disk.

To execute the project as a whole, execute `python fullprocess.py`
There is a script `execute_fullprocess.sh` that can be added to crontab 
and execute `fullprocess.py` on regular intervals within conda environment.


##### The logic behind the script `fullprocess.py`:

For every run of the script, random hex value is being generated. This value is inserted into 
the databse together with scores and file names so it is easy to identify
which are production values and which are historic values.


###### Step 1 
- The script checks for new datasets and if there are any, new datasets are ingested 
with `ingestion.py`

- Part of the reporting is checking and saving timing of two scripts. In this step we meassure
execution time of `ingestion.py` script


###### Step 2 
- Run predictions of the production model on new dataset with `diagnostics.py` -> `model_predictions()`

- We score the predictions with `scoring.py` -> `score_model()` and compare new F1 with F1 for 
production model

- If new F1 score is lower, we have a model drift and so we go with Step 3. 
Otherwise we end the program


###### Step 3
- Retrain the model on new dataset with `training.py` -> `train_model()`

- It's where the script meassures the execution timing again and saves it to the database  

- Predictions are done and new F1 score calculated and saved to the database as production ones

- New model is moved to prouction


###### Step 4

- In this step confucion matrix is generated

- There are statistic done for the dataset that are stored to the database:
	- mean, median and standard deviation for the festures
	- amount of NA for each dataset column
	
##### Step 5
Separately, as part of apicalls.py which has to be executed manually, there is a check done
for outdated packages `pip list --outdated`



#### Continuous diagnostics

There is a script called `execute_fullprocess.sh` which can be configured as cron job
and execute fullprocess.py in regular intervals.


### GitHub workflow config
There is GitHUb workflow configured to run on GitHub and and pre-commit script
that is executed locally and requires the scripts to pass flake8 command check
before the code is commited

### Contact
Project Link: https://github.com/MidnightSkyUniverse/dynamic_risk_assessment_system
API: https://risk-assess-sys.herokuapp.com/


## For Udacity Team
* As advised I save the data to a database. Since I wanted to run the project on Heroku,
I decided on postgreSQL database which is free on Heroku.

* I created a script to generate some random data so I can rerun the project

* API can be tested two ways
	* https://risk-assess-sys.herokuapp.com/ shows images stored during `fullprocess.py` execusion
	* https://risk-assess-sys.herokuapp.com/apireturns saves in `models/apireturns.txt` with
what was requested as part of the project. The list of outdated packes is emtpy assuming
the list of packages is short


