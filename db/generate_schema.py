import pymongo
FACTORIES = [
    {
        "factory":"竹",
        "longitude":121.01,
        "latitude":24.773,
        "Si":1.758,
        "Padj":1.0,
        "magnitude":[]

    },
    {
        "factory":"中",
        "longitude":120.618,
        "latitude":24.2115,
        "Si":1.063,
        "Padj":1.0,
        "magnitude":[]
    },
    {
        "factory":"南",
        "longitude":120.272,
        "latitude":23.1135,
        "Si":1.968,
        "Padj":1.0,
        "magnitude":[]
    }]

client = pymongo.MongoClient("mongodb://172.24.200.8:2047/")

# Connect to the "mydatabase" database
db = client["meteorological_center"]
collection = db["factory"]
result = collection.delete_many({})

for fac in FACTORIES:
    db['factory'].insert_one(fac)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
# 廠區 longitude latitude Si Padj
# 竹 121.01 24.773 1.758 1.0
# 中 120.618 24.2115 1.063 1.0
# 南 120.272 23.1135 1.968 1.0