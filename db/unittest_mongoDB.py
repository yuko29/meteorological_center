from mongoDB import mongoDB
import unittest

class MongoDBTest(unittest.TestCase):
    def setup(self):
        self.db = mongoDB()
    
    def test_insertEarthquake(self):
        pass
    
    def test_insertReservoir(self):
        pass
    
    def test_retrieveEarthquake(self):
        pass
    
    def test_retrieveReservoir(self):
        pass
    
    def test_retrieveElectricity(self):
        pass
    
    def test_retrieveFactoryEarthquake(self):
        pass
    


# db = mongoDB()
# earthquake_record = db.retrieveFactoryEarthquake(factory="Hsinchu")
# print(earthquake_record)
# electricity_record = db.retrieveElectricity(region="北")
# print(electricity_record)