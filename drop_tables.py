import psycopg2
import json

with open('config.json', 'r') as f:
    config = json.load(f)

DATABASE_URL = config['DATABASE_URL']

commands = [
"""drop table f1;""",
"""drop table feature_stats;""",
""" drop table ingested_files;""",
""" drop table missing_data ;""",
""" drop table script_timing;""",
]

def db_drop(commands):
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

if __name__ == '__main__':
    db_drop(commands)
