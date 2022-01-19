import psycopg2
import json
import os

with open('config.json', 'r') as f:
    config = json.load(f)


#DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = config['DATABASE_URL']


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = [
        """
        CREATE TABLE ingested_files (
            id SERIAL PRIMARY KEY,
            file CHAR(100) NOT NULL,
            hex CHAR(6) NOT NULL,
            created TIMESTAMPTZ
        )
        """,
        """
        CREATE TABLE f1 (
            id SERIAL PRIMARY KEY,
            f1_score REAL NOT NULL,
            hex CHAR(6) NOT NULL,
            created TIMESTAMPTZ
        )
        """,
        """
        CREATE TABLE feature_stats (
            id SERIAL PRIMARY KEY,
            feature CHAR(100) NOT NULL,
            mean REAL NOT NULL,
            median REAL NOT NULL,
            std REAL NOT NULL,
            hex CHAR(6) NOT NULL,
            created TIMESTAMPTZ
        )
        """,
        """
        CREATE TABLE missing_data (
            id SERIAL PRIMARY KEY,
            feature CHAR(100) NOT NULL,
            percentage REAL NOT NULL,
            hex CHAR(6) NOT NULL,
            created TIMESTAMPTZ
        )
        """,
        """
        CREATE TABLE pip_outdated (
            id SERIAL PRIMARY KEY,
            list TEXT NOT NULL,
            hex CHAR(6) NOT NULL,
            created TIMESTAMPTZ
        )
        """
]
    
    conn = None
    try:
        # connect to the PostgreSQL server
        """
        conn = psycopg2.connect(user=config.USER,
                                  password=config.PASSWORD,
                                  host="127.0.0.1",
                                  port="5432",
                                  database=config.DATABASE_NAME
        )
        """
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


if __name__ =='__main__':
    create_tables()
