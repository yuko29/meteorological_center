import pymongo

class mongoDB():
    def __init__(self):
        # Create a MongoClient object with the IP address of the MongoDB container
        self.client = pymongo.MongoClient("mongodb://172.30.58.128:27017/")

        # Connect to the "mydatabase" database
        self.db = self.client["mydatabase"]


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