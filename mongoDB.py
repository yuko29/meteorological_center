import pymongo
import json
from datetime import datetime
MAX_PRSERVE_RECORD = 100


class mongoDB():
    def __init__(self):
        # with open("./schema.json", "w") as f:
        #     self.schema = json.load(f)
        # for i in self.schema:
        #     self.collection['earthquake'] = i['collection_name']
        # Create a MongoClient object with the IP address of the MongoDB container
        self.client = pymongo.MongoClient("mongodb://172.28.138.245:2047/")
        # Connect to the "mydatabase" database
        self.db = self.client["meteorological_center"]
        self.earthquake = self.db['earthquake']
        self.reservoir = self.db['reservoir']
        self.electricity = self.db['electricity']
        self.earthquake.create_index("time")
        self.reservoir.create_index("time")
        self.electricity.create_index("time")



    def __dataValid(self, data, functName):
        if(functName == self.insertEarthquake.__name__):
            return type(data['time']) == str\
                    and type(data['M_L']) == float\
                    and type(data['focal_dep']) == float\
                    and type(data['longitude']) == float\
                    and type(data['latitude']) == float

        if(functName == self.insertReservoir.__name__):
            return type(data['name']) == str\
                    and type(data['water_supply']) == float\
                    and type(data['percentage']) == float\
                    and type(data['time']) == str\
        
        if(functName == self.insertElectricity.__name__):
            return type(data['region']) == str\
                    and type(data['power_usage']) == float\
                    and type(data['power_generate']) == float\
                    and type(data['time']) == str

    def insertEarthquake(self, data):
        print(data)
        try:
            assert self.__dataValid(data, self.insertEarthquake.__name__) == True
            data['time'] = datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
            self.earthquake.insert_one(data)
            return 0
        except KeyError as e:
            print(f"{e.__class__.__name__} on checking column {e.args}")
            return 1
        except Exception as e:
            print(f"{e.__class__.__name__} occured.")
            return 1

    def insertReservoir(self, data):
        print(data)
        try:
            assert self.__dataValid(data, self.insertReservoir.__name__) == True
            data['time'] = datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
            self.reservoir.insert_one(data)
            return 0
        except KeyError as e:
            print(f"{e.__class__.__name__} on checking column {e.args}")
            return 1
        except Exception as e:
            print(f"{e.__class__.__name__} occured.")
            return 1

    def insertElectricity(self, data):
        print(data)
        try:
            assert self.__dataValid(data, self.insertElectricity.__name__) == True
            data['time'] = datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
            self.reservoir.insert_one(data)
            return 0
        except KeyError as e:
            print(f"{e.__class__.__name__} on checking column {e.args}")
            return 1
        except Exception as e:
            print(f"{e.__class__.__name__} occured.")
            return 1

    def retrieveEarthquake(self, quantity=1):
        if quantity>MAX_PRSERVE_RECORD:
            print("Exceed")
        ret = self.earthquake.find().sort("time", -1).limit(min(quantity, MAX_PRSERVE_RECORD))
        return ret


    def retrieveElectricity(self, quantity=1):
        if quantity>MAX_PRSERVE_RECORD:
            print("Exceed")
        ret = self.electricity.find().sort("time", -1).limit(min(quantity, MAX_PRSERVE_RECORD))
        return ret

    def retrieveReservoir(self, quantity=1):
        if quantity>MAX_PRSERVE_RECORD:
            print("Exceed")
        ret = self.reservoir.find().sort("time", -1).limit(min(quantity, MAX_PRSERVE_RECORD))
        return ret



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
        