import psycopg2
from psycopg2 import Error
import os
from urllib.parse import urlparse


#Connect to an existing database
#db_url = os.environ.get("DATABASE_URL")
db_url = "postgres://unylehihjuqcgh:44ce4b00a69887680646812ba372fa6bbfc1348bc1339bd37649f5e7d8248634@ec2-99-80-170-190.eu-west-1.compute.amazonaws.com:5432/ddelk8o88jn4dn"
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

#db_user = os.environ.get("DB_USER")
#db_pw = os.environ.get("DB_PW")
#db_host = os.environ.get("DB_HOST")
#db_port = os.environ.get("DB_PORT")
#db_name = os.environ.get("DB_NAME")
#def conn():
#    connection = psycopg2.connect(
#                                user=db_user,
#                                password=db_pw,
#                                host=db_host,
#                                port=db_port,
#                                database=db_name
#                                )
#    return connection



def createT():
    created = False
    con = conn()
    cur = con.cursor()
    create_table = """
                    CREATE TABLE xp_event
                    (DATE    TEXT    PRIMARY KEY    NOT NULL,
                    LOG    JSONB    NOT NULL);
                    """
    try:
        cur.execute(create_table)
        con.commit()
    except psycopg2.Error as error:
        print(f'error occured\n{error}')
    else:
        created = True
        cur.close()
        con.close()
    finally:
        return created


def insert(t_date,e_log):
    inserted = False
    con = conn()
    cur = con.cursor()
    insert_query =  """ 
                    INSERT INTO xp_event (DATE,LOG) 
                    VALUES (%s,%s)
                    """
    try:
        cur.execute(insert_query,(t_date,e_log,))
        con.commit()
    except psycopg2.Error as error:
        print(f'error occured\n{error}')
    else:
        inserted = True
        cur.close()
        con.close()
    finally:
        return inserted

def update(t_date,e_log):
    updated = False
    con = conn()
    cur = con.cursor()
    update_query =   """Update xp_event 
                        set log = %s 
                        where date = %s """
    try:
        cur.execute(update_query,(e_log,t_date,))
        con.commit()
    except psycopg2.Error as error:
        print(f'error occured\n{error}')
    else:
        updated = True
        cur.close()
        con.close()
    finally:
        return updated

def retrieve(t_date):
    con = conn()
    cur = con.cursor()
    retrieve_query= """
                    SELECT xp_event 
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

