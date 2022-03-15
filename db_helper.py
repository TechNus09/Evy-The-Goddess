import psycopg2
from psycopg2 import Error
import os
from urllib.parse import urlparse


# Connect to an existing database
#db_url = os.environ.get("DATABASE_URL")
#result = urlparse(db_url)
#username = result.username
#password = result.password
#database = result.path[1:]
#hostname = result.hostname
#port = result.port
#def conn():
#    connection = psycopg2.connect(
#                                    database = database,
#                                    user = username,
#                                    password = password,
#                                    host = hostname,
#                                    port = port
#                                )
#    return connection
db_user = os.environ.get("DB_USER")
db_pw = os.environ.get("DB_PW")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")
def conn():
    connection = psycopg2.connect(
                                user=db_user,
                                password=db_pw,
                                host=db_host,
                                port=db_port,
                                database=db_name
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

def update(t_date,e_log):
    r = False
    con = conn()
    print("con created")
    cur = con.cursor()
    print("cur created")
    update_query =   """Update logs 
                        set log = %s 
                        where date = %s """
    print("query created")
    try:
        cur.execute(update_query,(e_log,t_date,))
        print("query excuted")
        con.commit()
        print("cur commited")
    except psycopg2.Error as e:
        print(f'error occured\n{e}')
    else:
        r = True
        cur.close()
        print("cur closed")
        con.close()
        print("con closed")
    print(f" updated : "+str(r))
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

#member_temp = { 'ign' : 'name' , 'combat_xp' : 0 , 'mining_xp' : 0 , 'smithing_xp' : 0 , 'woodcutting_xp': 0 , 'crafting_xp' : 0 , 'fishing_xp' : 0 , 'cooking_xp' : 0 , 'total': 0}
#
#s = update('9999',member_temp)
#if s:
#    print("updated")