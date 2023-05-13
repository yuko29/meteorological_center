import pymongo

# Create a MongoClient object with the IP address of the MongoDB container
client = pymongo.MongoClient("mongodb://172.30.58.128:27017/")

# Connect to the "mydatabase" database
db = client["mydatabase"]

# Connect to the "mycollection" collection
col = db["mycollection"]

# Insert a document into the collection
document = {"name": "John", "age": 30}
col.insert_one(document)

# Find all documents in the collection
for document in col.find():
    print(document)