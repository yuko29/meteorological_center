import unittest
from DataBase import Database
import pymongo
import json
import math
from datetime import datetime
from db_config import IP, PORT, MAX_PRSERVE_RECORD
from unittest.mock import MagicMock

class MongoDBTest(unittest.TestCase):

    def setUp(self):
        self.instance = Database(IP = IP, PORT = PORT, db_name="my-mongodb")
        with open("./TDD1.json", "r") as f:
            self.test_cases = json.load(f)

    def __tearDown(self, collection_name):
        self.instance.db[collection_name].drop()


    def test_insertData(self):
        self.setUp()
        cases =[
            {
                "collection":"a_collection",
                "name":"Andy",
                "sex":"Male",
                "money":32
            },
            {
                "collection":"a_collection",
                "name":"Nina",
                "sex":0,
                "money":"32"
            }
        ]
        for case in cases:
            self.__tearDown(case['collection'])
            self.instance.retrieve_data = MagicMock(side_effect=self.instance.db[case["collection"]].find)
            self.instance.insert_data(case["collection"], case)
            retrieved_data = [x for x in self.instance.retrieve_data({}, {})][0]
            print(case)
            print(retrieved_data)
            self.assertEqual(case, retrieved_data)

    #def retrieve_data(self, collection, condition = {}, value = {"_id":0}, sort=('_id',1), limit=1):

if __name__ == "__main__":
    unittest.main()