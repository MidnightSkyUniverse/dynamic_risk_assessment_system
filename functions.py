"""
    Author: Ali Binkowska
    Date: Jan 2022

    Collection of functions used through the pipeline
"""
import pandas as pd
import json
import random
import subprocess
import psycopg2
import os

# Save the link to Heroku database, the link can change between session
try:
    DATABASE_URL = os.environ['DATABASE_URL']
except:
    DATABASE_URL = subprocess.check_output(['heroku', 'config:get', 'DATABASE_URL', '-a', 'risk-assess-sys']).decode('utf8').strip()


with open('config.json', 'r') as f:
    config = json.load(f)

label = config['label']
numeric_cols = config['numeric_cols']


def db_insert(commands):
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    
def db_select(command):
    conn = None
    record = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # Fetch result
        record = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return record

def set_f1_as_production(hex_value):
    conn = None
    record = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # create table one by one
        command = "update f1 set is_production = False;"
        cur.execute(command)
        command = f"update f1 set is_production = True  where hex='{hex_value}';"
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def random_hex():
    return "{:06x}".format(random.randint(0, 0xFFFFFF))


def process_data(file_path):
    """
    Read cvs file and split the dataset into X and y
    """
    trainingdata = pd.read_csv(file_path)
    X = trainingdata.loc[:, numeric_cols].values.reshape(-1, len(numeric_cols))
    y = trainingdata[label].values.reshape(-1, 1).ravel()

    return (X, y)


def execute_command(cmd_list):
    """
    Function execute command and returns stdout as a list

    input: command as a list ex ['pip','list','--outdated']
    """
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
    results = []
    while True:
        output = process.stdout.readline()
        if output.decode('utf8') == '' and process.poll() is not None:
            break
        if output:
            results.append(output.decode('utf8').strip().split())
    rc = process.poll()

    return results
