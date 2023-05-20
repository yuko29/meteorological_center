self.client = pymongo.MongoClient("mongodb://172.28.138.245:2047/")

with open("./insert_schema.json", "r") as f:
    self.insert_schema = json.load(f)

self.mapper = {
    self.insertEarthquake.__name__:"earthquake",
    self.insertElectricity.__name__:"electricity",
    self.insertReservoir.__name__:"reservoir"
}




# Connect to the "mydatabase" database
self.db = self.client["meteorological_center"]
self.db['earthquake'].insert_one()
self.db['reservoir'].create_index("time")
self.db['electricity'].create_index("time")