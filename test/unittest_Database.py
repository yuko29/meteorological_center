from Database import Database
import unittest
from unittest.mock import patch, Mock, MagicMock
from strongtyping.strong_typing_utils import TypeMisMatch


class TestDatabase(unittest.TestCase):
    @patch("pymongo.MongoClient")
    def setUp(self, mock_MongoClient):
        self.app = Database(ip="123", port=123, db_name="test")
        self.app.client = mock_MongoClient
        self.app.db = self.app.client["mock"]

    def tearDown(self):
        pass

    def test_insert_data_input_typechecking(self):
        with self.assertRaises(TypeMisMatch):  # Test collection_name is not str
            self.app.insert_data(collection_name=1, data={})

        with self.assertRaises(TypeMisMatch):  # Test data is not dict
            self.app.insert_data(collection_name="test", data="test")

    def test_retrieve_data_input_typechecking(self):
        with self.assertRaises(TypeMisMatch):  # Test collection_name is not str
            self.app.retrieve_data(collection_name=1)

        with self.assertRaises(TypeMisMatch):  # Test condition is not dict
            self.app.retrieve_data(collection_name="test", condition="test")

        with self.assertRaises(TypeMisMatch):  # Test value is not dict
            self.app.retrieve_data(collection_name="test", value="test")

        with self.assertRaises(TypeMisMatch):  # Test sort is not tuple
            self.app.retrieve_data(collection_name="test", sort="test")

    @patch("pymongo.collection.Collection.insert_one")
    def test_insert_data_(self, mock_insert_one):
        self.app.insert_data(collection_name="test", data={})

    @patch("pymongo.collection.Collection.find")
    def test_retrieve_data_(self, mock_find):
        self.app.retrieve_data(collection_name="test", condition={}, value={})


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
