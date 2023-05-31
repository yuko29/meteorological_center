import pymongo
import json
import math
from datetime import datetime
from db_config import IP, PORT, MAX_PRSERVE_RECORD

"""
    This class is an abstract database's API to connect mongoDB.
    Since we use docker container to host mongoDB, 
    port and IP of the container are required in order to connect to it.
    Instead of directly used it, 
    you are recommaned to inherit this class to implement your custom database.
"""

class Database():
    def __init__(self, IP: str, PORT: int, db_name: str, collection_list = None):
        self.client = pymongo.MongoClient(f"mongodb://{IP}:{PORT}/")
        self.__collection_list = [] # list
        self.db = self.client[db_name]   # init database
        if collection_list != None:
            for i in collection_list:
                self.db["i"]={}

    def insert_data(self, collection_name: str, data: dict):
        self.db[collection_name].insert_one(data)

    def retrieve_data(self, collection, condition = {}, value = {"_id":0}, sort=('_id',1), limit=1):
        return self.db[collection].find(condition, value).sort(sort[0], sort[1]).limit(limit)
