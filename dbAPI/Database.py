import pymongo
from strongtyping.strong_typing import match_class_typing

"""
    This class is an abstract database's API to connect mongoDB.
    Since we use docker container to host mongoDB,
    port and IP of the container are required in order to connect to it.
    Instead of directly used it,
    you are recommaned to inherit this class to implement your custom database.
"""

@match_class_typing
class Database():
    def __init__(self, ip: str, port: int, db_name: str):
        self.client = pymongo.MongoClient(f"mongodb://{ip}:{port}/")
        self.db = self.client[db_name]   # init database

    def insert_data(self, collection_name: str, data: dict):
        self.db[collection_name].insert_one(data)

    def retrieve_data(
        self, collection_name: str, condition: dict = {},
        value: dict = {"_id": 0}, sort: tuple = ('_id', 1), limit: int = 1
    ):
        temp = self.db[collection_name].find(condition, value)
        result = temp.sort(sort[0], sort[1]).limit(limit)
        return result