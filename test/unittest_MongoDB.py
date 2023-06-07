from MongoDB import MongoDB
from Database import Database
import unittest
from unittest.mock import patch, Mock, MagicMock
from strongtyping.strong_typing_utils import TypeMisMatch
from datetime import datetime

"""
I want to mock the parent class of MongoDB (Database)
so that I can test the methods in MongoDB without 
actually connecting to the database.
"""


class TestMongoDB(unittest.TestCase):
    @patch("pymongo.MongoClient")
    def setUp(self, mock_Database):
        self.app = MongoDB(
            ip="123", port=123, db_name="test", collection_list=["test_colleciont"]
        )

    def tearDown(self):
        pass

    # ------ check args data type ------ #
    @patch("pymongo.MongoClient")
    def test_illegal_init(self, mock_mongo_client):
        # with self.assertRaises(TypeMisMatch):  # Wrong args type
        self.app = MongoDB(
            ip="123", port=None, db_name="test", collection_list=["test_colleciont"]
        )

    @patch("pymongo.collection.Collection.insert_one")
    def test_insert_earthquake_data(self, mock_insert_one):
        with self.assertRaises(TypeMisMatch):  # Wrong args type
            self.app.insert_earthquake_data(
                {
                    "_id": 8787,
                    "time": 123,
                    "factory": "中",
                    "magnitude": [
                        {"factory": "竹", "magnitude": 0.00032644588703523386},
                        {"factory": "中", "magnitude": 0.00019905740360289052},
                        {"factory": "南", "magnitude": 0.0003714193582435097},
                    ],
                }
            )

        with self.assertRaises(KeyError):  # Missing key
            self.app.insert_earthquake_data(
                {
                    "time": "2023-05-12 03:40:52",
                    "factory": 123,
                    "magnitude": [
                        {"magnitude": 0.00032644588703523386},
                        {"factory": "中", "magnitude": 0.00019905740360289052},
                        {"factory": "南", "magnitude": 0.0003714193582435097},
                    ],
                }
            )

        self.app.insert_earthquake_data(
            {
                "_id": 8787,
                "time": datetime.now(),
                "factory": "中",
                "magnitude": [
                    {"factory": "竹", "magnitude": 0.00032644588703523386},
                    {"factory": "中", "magnitude": 0.00019905740360289052},
                    {"factory": "南", "magnitude": 0.0003714193582435097},
                ],
            }
        )

    @patch("pymongo.collection.Collection.insert_one")
    def test_insert_electricity_data(self, mock_insert_one):
        # Wrong args type
        with self.assertRaises(TypeMisMatch):
            self.app.insert_electricity_data(
                {
                    "time": "",
                    "region": "中",
                    "power_usage": "0.1",
                    "power_generate": "0.2",
                }
            )

        # Normal case
        self.app.insert_electricity_data(
            {
                "time": datetime.now(),
                "region": "中",
                "power_usage": 0.1,
                "power_generate": 0.2,
            }
        )

    @patch("pymongo.collection.Collection.insert_one")
    def test_insert_reservoir_data(self, mock_insert_one):
        # Wrong args type
        with self.assertRaises(TypeMisMatch):
            self.app.insert_reservoir_data(
                {"time": "", "name": "德基水庫", "percentage": "0.1", "water_supply": "0.2"}
            )

        # Normal case
        self.app.insert_reservoir_data(
            {
                "time": datetime.now(),
                "name": "德基水庫",
                "percentage": 0.1,
                "water_supply": 0.2,
            },
        )

    @patch("pymongo.collection.Collection.find")
    def test_retrieve_earthquake_data(self, mock_find):
        # Wrong args type
        with self.assertRaises(TypeMisMatch):
            self.app.retrieve_earthquake_data(quantity="1")

        # Normal case
        self.app.retrieve_earthquake_data(quantity=1)

    @patch("pymongo.collection.Collection.find")
    def test_retrieve_earthquake_data_by_factory(self, mock_find):
        # Wrong args type
        with self.assertRaises(TypeMisMatch):
            self.app.retrieve_earthquake_data_by_factory(factory="竹", quantity="1")

        # Normal case
        self.app.retrieve_earthquake_data_by_factory(factory="竹", quantity=1)

    @patch("pymongo.collection.Collection.find")
    def test_retrieve_electricity_data_by_region(self, mock_find):
        # Wrong args type
        with self.assertRaises(TypeMisMatch):
            self.app.retrieve_electricity_data_by_region(region="竹", quantity="1")

        # Normal case
        self.app.retrieve_electricity_data_by_region(region="竹", quantity=1)

    @patch("pymongo.collection.Collection.find")
    def test_retrieve_reseroir_data_by_name(self, mock_find):
        # Wrong args type
        with self.assertRaises(TypeMisMatch):
            self.app.retrieve_reservoir_data_by_name(name="德基水庫", quantity="1")

        # Normal case
        self.app.retrieve_reservoir_data_by_name(name="德基水庫", quantity=1)


if __name__ == "__main__":
    unittest.main()
