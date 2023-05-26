import pymongo
import json
import math
from datetime import datetime
MAX_PRSERVE_RECORD = 100


class mongoDB():

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://172.17.229.144:2047/")

        with open("./insert_schema.json", "r") as f:
            self.insert_schema = json.load(f)

        self.mapper = {
            self.insertEarthquake.__name__:"earthquake",
            self.insertElectricity.__name__:"electricity",
            self.insertReservoir.__name__:"reservoir"
        }

        # Connect to the "mydatabase" database
        self.db = self.client["meteorological_center"]
        self.db['earthquake'].create_index("time")
        self.db['reservoir'].create_index("time")
        self.db['electricity'].create_index("time")


    def filterAnomaly(self, data):
        t = {}
        for key, value in data.items():
            if value == -1.0 or value == "-":
                continue
            else:
                t[key]=value
        return t

    def __dataValid(self, data, functName):
        insert_schema_table = None
        for collection_schema in self.insert_schema:
            if(collection_schema['collection_name'] == self.mapper[functName]):
                insert_schema_table = collection_schema['schema']
                break
            
        for var, _type in insert_schema_table.items():
            if type(data[var]) != eval(_type):
                return False
        return True

    def insertEarthquake(self, data):
        data['time'] = datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
        assert self.__dataValid(data, self.insertEarthquake.__name__) == True
        data = self.filterAnomaly(data)
        magnitude = data.pop('magnitude')
        print(data)
        self.db['earthquake'].insert_one(data)
        factories = self.db['factory'].find()
        for fac in factories:
            for data_fac in magnitude:
                if(fac['factory'] == data_fac['factory']):
                    data['magnitude']=data_fac['magnitude']
                    self.db['factory'].update_one(
                        {"factory":fac['factory']},
                        {"$push":{"magnitude":data}}
                    )
                    break

        return 0

    def insertReservoir(self, data):
        data['time'] = datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
        assert self.__dataValid(data, self.insertReservoir.__name__) == True
        data = self.filterAnomaly(data)
        try:
            name = data.pop("name")
        except KeyError as e:
            print(f"Insertion failed. Reservoir name is not provided.")
            return
        if len(list(self.db['reservoir'].find({"name":name}))) == 0:
            self.db['reservoir'].insert_one(
                {
                    "name":name,
                    "data":[]
                }
            )

        self.db['reservoir'].update_one(
            {"name":name},
            { "$push":{"data":data}}
        )

        return 0

    def insertElectricity(self, data):
        data['time'] = datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
        assert self.__dataValid(data, self.insertElectricity.__name__) == True
        data = self.filterAnomaly(data)
        try:
            region = data.pop('region')
        except KeyError as e:
            print(f"Insertion failed. region name is not provided.")
            return
        if len(list(self.db['electricity'].find({"region":region}))) == 0:
            self.db['electricity'].insert_one(
                {
                    "region":region,
                    "data":[]
                }
            )

        self.db['electricity'].update_one(
            {"region":region},
            { "$push":{"data":data}}
        )

        return 0

    def retrieveEarthquake(self, quantity=1):
        if quantity>MAX_PRSERVE_RECORD:
            raise Exception("requested quantity exceed.")
        ret = self.db['earthquake'].find().sort("time", -1).limit(min(quantity, MAX_PRSERVE_RECORD))
        return ret


    def retrieveFactoryEarthquake(self, quantity=1, factory=None):
        if factory == None:
            raise Exception("factory not specified.")
        if quantity>MAX_PRSERVE_RECORD:
            raise Exception("requested quantity exceed.")
        else:
            ret = self.db['factory'].find({"factory":factory},{"magnitude":1, "_id":0}).limit(min(quantity, MAX_PRSERVE_RECORD))
            ret = list(ret)[0]['magnitude']
            return ret


    def retrieveElectricity(self, quantity=1, region=None):
        if region == None:
            raise Exception("region not specified.")
            
        if quantity>MAX_PRSERVE_RECORD:
            raise Exception("requested quantity exceed.")

        ret = self.db['electricity'].find({"region":region},{"data":1, "_id":0}).limit(min(quantity, MAX_PRSERVE_RECORD))
        ret = list(ret)[0]["data"]
        return ret

    def retrieveReservoir(self, quantity=1, name=None):
        if name == None:
            raise Exception("reservoir not specified.")
        if quantity>MAX_PRSERVE_RECORD:
            raise Exception("requested quantity exceed.")
        ret = self.db['reservoir'].find({"name":name},{"data":1, "_id":0}).sort("time", -1).limit(min(quantity, MAX_PRSERVE_RECORD))
        ret = list(ret)[0]["data"]
        return ret


    def reset(self):
        collection = self.db["earthquake"]
        # Delete all documents in the collection
        result = collection.delete_many({})
        collection = self.db["electricity"]
        result = collection.delete_many({})
        collection = self.db["reservoir"]
        result = collection.delete_many({})
        collection = self.db["factory"]
        for fac in collection.find({}):
            collection.update_one({"factory":fac['factory']},{"$set":{"magnitude":[]}})



# const session = db.getMongo().startSession();
# session.startTransaction();

# try {
#   // Read the documents and count the size within the transaction
#   const documents = db.yourCollectionName.find({}, { projection: { _id: 1 } }).toArray();
#   const collectionSize = documents.length;

#   if (collectionSize > 100) {
#     // Sort the documents by _id and delete the oldest document
#     const oldestDocument = db.yourCollectionName.findOneAndDelete(
#       {},
#       { sort: { _id: 1 }, collation: { locale: "en_US", numericOrdering: true } }
#     );

#     // Commit the transaction
#     session.commitTransaction();

#     // Use the `oldestDocument` if needed for further processing or logging
#   } else {
#     // Abort the transaction if the collection size is not greater than 100
#     session.abortTransaction();
#   }
# } finally {
#   // End the transaction and release the session
#   session.endSession();
# }






    def exampleAPI(self):
        # Connect to the "mycollection" collection
        col = self.db["mycollection"]

        # Insert a document into the collection
        document = {"name": "John", "age": 30}
        col.insert_one(document)

    def exampleAPI2(self):
        col = self.db["mycollection"]
        # Find all documents in the collection
        for document in col.find():
            print(document)
