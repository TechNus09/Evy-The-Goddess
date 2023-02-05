import os

import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection







class DbHelper():
    """Helper Class for working with MongoDB
    ps: storing document in format of {"_id":"doc_id","doc_id":your_document_here(json_formatted)}"""
    def __init__(self,db_url:str,db_name:str=None,collection_name:str=None) -> None:
        self.client:MongoClient = MongoClient(db_url)
        self.db:Database = self.client[db_name]
        self.coll:Collection = self.db[collection_name]
        pass


    def create_record(self,record_id:str,record:dict) -> bool:
        """insert new record to collection"""
        inserted = False
        try:
            self.coll.insert_one({"_id":record_id,record_id:record})
            inserted = True
        except Exception as e:
            print(e)
        
        return inserted

    def view_record(self,record_id:str) -> dict:
        """retrieve the record of the given id"""
        record:dict = self.coll.find_one({"_id":f"{record_id}"})
        record.pop("_id")
        return record[record_id]

    def update_record(self,record_id:str,new_record:dict) -> bool:
        """update the record of the given id to a new given record"""
        updated = False
        try:
            self.coll.update_one({"_id":f"{record_id}"},{"$set":{record_id:new_record}})
            updated = True
        except Exception as e :
            print(e)
        
        return updated

    def delete_record(self,record_id:str) -> bool:
        """delete the record of the given id"""
        deleted = False
        try:
            record:dict = self.coll.delete_one({"_id":f"{record_id}"})
            deleted = True
        except Exception as e :
            print(e)

        return deleted











