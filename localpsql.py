import psycopg2
import os

#DATABASE_URL = os.environ.get("DATABASE_URL")
#DATABASE_URL='postgres://nfksqgpxwfhaiu:f8b71573ae408df91b69c635f0f5044955eac05df1a8fe6bccf6bec901339a91@ec2-54-220-243-77.eu-west-1.compute.amazonaws.com:5432/d7o2kqmfdk6m6j'
DATABASE_URL="postgresql:///admin"
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

cur.execute('SELECT version()')

version = cur.fetchone()[0]
print(version)
