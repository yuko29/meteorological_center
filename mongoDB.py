import pymongo
import json
from datetime import datetime
MAX_PRSERVE_RECORD = 100


class mongoDB():


    def __init__(self):
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
        self.db['earthquake'].create_index("time")
        self.db['reservoir'].create_index("time")
        self.db['electricity'].create_index("time")

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
        self.db['earthquake'].insert_one(data)
        return 0

    def insertReservoir(self, data):
        data['time'] = datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
        assert self.__dataValid(data, self.insertReservoir.__name__) == True
        name = data.pop("name")

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
        region = data.pop('region')
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
            print("Exceed")
        ret = self.db['earthquake'].find().sort("time", -1).limit(min(quantity, MAX_PRSERVE_RECORD))
        return ret


    def retrieveElectricity(self, quantity=1, region="北"):
        if quantity>MAX_PRSERVE_RECORD:
            print("Exceed")
        #ret = self.db['electricity'].find({"region":region}).sort("time", -1).limit(min(quantity, MAX_PRSERVE_RECORD))
        ret = self.db['electricity'].find({})
        return ret

    def retrieveReservoir(self, quantity=1, name="德基水庫"):
        if quantity>MAX_PRSERVE_RECORD:
            print("Exceed")
        ret = self.db['reservoir'].find({"name":name}).sort("time", -1).limit(min(quantity, MAX_PRSERVE_RECORD))
        return ret


    def reset(self):
        collection = self.db["earthquake"]
        # Delete all documents in the collection
        result = collection.delete_many({})
        collection = self.db["electricity"]
        result = collection.delete_many({})
        collection = self.db["reservoir"]
        result = collection.delete_many({})
        result = self.db["mycollection"]
        result = collection.delete_many({})


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
        