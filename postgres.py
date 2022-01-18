#import the relevant sql library 
from sqlalchemy import create_engine
import pandas as pd 

# link to your database
URI = 'postgresql://nfksqgpxwfhaiu:f8b71573ae408df91b69c635f0f5044955eac05df1a8fe6bccf6bec901339a91@ec2-54-220-243-77.eu-west-1.compute.amazonaws.com:5432/d7o2kqmfdk6m6j'
engine = create_engine(URI, echo = False)

# attach the data frame (df) to the database with a name of the 
# table; the name can be whatever you like
df = pd.read_csv("ingesteddata/finaldata.csv")
df.to_sql("phil_nlp", con = engine, if_exists="append")

# run a quick test 
print(engine.execute("SELECT * FROM phil_nlp").fetchone())
