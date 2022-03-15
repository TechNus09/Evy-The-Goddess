import psycopg2
from psycopg2 import Error
import os
from urllib.parse import urlparse


# Connect to an existing database
db_url = os.environ.get("DATABASE_URL")
result = urlparse(db_url)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port
def conn():
    connection = psycopg2.connect(
                                    database = database,
                                    user = username,
                                    password = password,
                                    host = hostname,
                                    port = port
                                )
    return connection


def createT():
    con = conn()
    cur = con.cursor()
    create_table = """
                    CREATE TABLE logs
                    (DATE    TEXT    PRIMARY KEY    NOT NULL,
                    LOG    JSONB    NOT NULL);
                    """
    cur.execute(create_table)
    con.commit()
    cur.close()
    con.close()
    return True



def insert(t_date,e_log):
    con = conn()
    cur = con.cursor()
    insert_query = """ 
                    INSERT INTO logs (DATE,LOG) 
                    VALUES (%s,%s)
                    """
    cur.execute(insert_query,(t_date,e_log,))
    con.commit()
    cur.close()
    con.close()
    return True

def update(e_log,t_date):
    r = False
    try:
        con = conn()
        print("con created")
        cur = con.cursor()
        print("cur created")
        update_query =   """Update logs 
                            set log = %s 
                            where date = %s """
        print("query created")
        cur.execute(update_query,(e_log,t_date))
        print("query excuted")
        con.commit()
        print("cur commited")
    except psycopg2.OperationalError as e:
        print('error occured\n{0}').format(e)
    else:
        r = True
        cur.close()
        print("cur closed")
        con.close()
        print("con closed")
    return r


def retrieve(t_date):
    con = conn()
    cur = con.cursor()
    retrieve_query= """
                    SELECT log 
                    FROM logs 
                    WHERE date = %s 
                    """
    cur.execute(retrieve_query,(t_date,))
    row = cur.fetchone()
    while row is not None:
        log = row
        row = cur.fetchone()
    con.commit()
    cur.close()
    con.close()
    return dict(log[0])

