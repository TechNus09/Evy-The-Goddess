from pprint import pprint
from db_helper import *
from evy_helper import *


def insert_player(player_name:str,data:dict):
    updated = False
    try:
        log = retrieve("0000")
        log[player_name]=data
        update("0000",jsing(log))
        updated = True
    except :
        updated = False
    return updated

