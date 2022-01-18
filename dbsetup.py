import psycopg2
import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = [
        """
        CREATE TABLE f1 (
            f1_id SERIAL PRIMARY KEY,
            f1_score REAL NOT NULL,
            created TIMESTAMPTZ
        )
        """]
    
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(user=config.USER,
                                  password=config.PASSWORD,
                                  host="127.0.0.1",
                                  port="5432",
                                  database=config.DATABASE_NAME
        )
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
