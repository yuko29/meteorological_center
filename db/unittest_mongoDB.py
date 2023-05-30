# from mongoDB import mongoDB
# import unittest
# import json


# class MongoDBTest(unittest.TestCase):
#     def setup(self):
        
#         self.db = mongoDB()
#         with open("./test_cases.json", "r") as f:
#             self.test_cases = json.load(f)
    
#     def test_insertEarthquake(self):
#         self.setup()
#         print(self.test_cases)
#         pass
    
#     def test_insertReservoir(self):
#         pass
    
#     def test_retrieveEarthquake(self):
#         pass
    
#     def test_retrieveReservoir(self):
#         pass
    
#     def test_retrieveElectricity(self):
#         pass
    
#     def test_retrieveFactoryEarthquake(self):
#         pass
    
# if __name__ == '__main__':
#     db = mongoDB()
#     unittest.main()

# # db = mongoDB()
# # earthquake_record = db.retrieveFactoryEarthquake(factory="Hsinchu")
# # print(earthquake_record)
# # electricity_record = db.retrieveElectricity(region="北")
# # print(electricity_record)

import json
import unittest
from mongoDB import mongoDB
from datetime import datetime

class MongoDBTestCase(unittest.TestCase):
    def setUp(self):
        self.db = mongoDB()
        with open("./test_cases.json", "r") as f:
            self.test_cases = json.load(f)

    def tearDown(self):
        # Clean up any created data in the database
        self.db.reset()
    
    def test_insertEarthquake(self):
        datas = self.test_cases['earthquake']
        for i in datas:
            if i['magnitude'] == None:
                with self.assertRaises(KeyError):
                    self.db.insertEarthquake(i)
            try:
                datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S")
            except:
                with self.assertRaises(ValueError):
                    self.db.insertEarthquake(i)
            if i['magnitude'] == None:
                with self.assertRaises(KeyError):
                    self.db.insertEarthquake(i)

            
            print(type(i['time']))
            #if(type(i)!=)2023-5-12 03:40:52
            print(i)
            self.db.insertEarthquake(i)
        self.assertEqual(self.db.insertEarthquake(data), 0)
        retrieved_data = self.db.retrieveEarthquake(quantity=1)
        self.assertEqual(len(retrieved_data), 1)
        self.assertDictEqual(retrieved_data[0], data)
    
    def test_insertReservoir(self):
        data = {
            "name": "Reservoir1",
            "time": "2023-05-30 10:00:00",
            "percentage": 80.0,
            "water_supply": 500.0
        }
        self.assertEqual(self.db.insertReservoir(data), 0)
        retrieved_data = self.db.retrieveReservoir(quantity=1, name="Reservoir1")
        self.assertEqual(len(retrieved_data), 1)
        self.assertDictEqual(retrieved_data[0], data)
    
    def test_insertElectricity(self):
        data = {
            "region": "North",
            "time": "2023-05-30 11:00:00",
            "power_usage": 1000.0,
            "power_generate": 800.0
        }
        self.assertEqual(self.db.insertElectricity(data), 0)
        retrieved_data = self.db.retrieveElectricity(quantity=1, region="North")
        self.assertEqual(len(retrieved_data), 1)
        self.assertDictEqual(retrieved_data[0], data)
    
    def test_retrieveFactoryEarthquake(self):
        data = {
            "factory": "Factory1",
            "time": "2023-05-30 12:00:00",
            "M_L": 4.5,
            "focal_dep": 8.2,
            "longitude": 120.0,
            "latitude": 23.5,
            "magnitude": 6.0
        }
        self.assertEqual(self.db.insertEarthquake(data), 0)
        retrieved_data = self.db.retrieveFactoryEarthquake(quantity=1, factory="Factory1")
        self.assertEqual(len(retrieved_data), 1)
        self.assertDictEqual(retrieved_data[0], {"magnitude": [data]})
    
    def test_reset(self):
        data = {
            "time": "2023-05-30 13:00:00",
            "M_L": 5.0,
            "focal_dep": 9.0,
            "longitude": 122.0,
            "latitude": 24.0
        }
        self.assertEqual(self.db.insertEarthquake(data), 0)
        self.db.reset()
        retrieved_data = self.db.retrieveEarthquake(quantity=1)
        self.assertEqual(len(retrieved_data), 1)
        self.assertDictEqual(retrieved_data[0], {
            "time": None,
            "M_L": -1.0,
            "focal_dep": -1.0,
            "longitude": -1.0,
            "latitude": -1.0
        })

if __name__ == '__main__':
    unittest.main()
