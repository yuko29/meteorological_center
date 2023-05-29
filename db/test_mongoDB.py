import unittest
from dbAPI.mongoDB import mongoDB

stab_earthquake = [
    {'time': '2023-5-12 03:40:52', 'M_L': 3.6, 'focal_dep': 3.2, 'longitude': 41.0, 'latitude': 20.7, 'magnitude': [{'factory': '竹', 'magnitude': 0.00032644588703523386}, {'factory': '中', 'magnitude': 0.00019905740360289052}, {'factory': '南', 'magnitude': 0.0003714193582435097}]},
    {}
]

class MongoDBTest(unittest.TestCase):
    instance = mongoDB()



    def test_insertEarthquake(self, testData):
        
    


a.insertEarthquake(earthEqake_test)
a.insertEarthquake(earthEqake_test2)
a.insertElectricity(electricity_test)
a.insertElectricity(electricity_test2)
a.insertReservoir(reservoir_test)
a.insertReservoir(reservoir_test2)
