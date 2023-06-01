import unittest
from Database import Database
import pymongo
import json
import math
from datetime import datetime
from db_config import IP, PORT, MAX_PRSERVE_RECORD
from unittest.mock import MagicMock

class MongoDBTest(unittest.TestCase):

    def set_up(self):
        self.instance = Database(ip = IP, port = PORT, db_name="my-mongodb")
        with open("./testcase_DataBase.json", "r") as f:
            self.test_cases = json.load(f)

    def __tear_down(self, collection_name):
        self.instance.db[collection_name].drop()


    def test_insert_data(self):
        self.set_up()
        cases = self.test_cases['Insert']
        for case in cases:
            self.__tear_down(case['collection'])
            self.instance.retrieve_data = MagicMock(side_effect=self.instance.db[case["collection"]].find)
            self.instance.insert_data(case["collection"], case)
            retrieved_data = [x for x in self.instance.retrieve_data({}, {})][0]
            self.assertEqual(case, retrieved_data)


    def test_retrieveData(self):
        self.set_up()
        cases = self.test_cases['Retrieve']
        for case in cases:
            self.__tear_down(case['collection'])
            self.instance.insert_data(case["collection"], case)
            ret = [x for x in self.instance.retrieve_data(case["collection"], condition = {}, value = {})][0]
            self.assertEqual(ret, case)


if __name__ == "__main__":
    unittest.main()