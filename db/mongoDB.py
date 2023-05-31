import pymongo
import json
import math
from datetime import datetime
from db_config import IP, PORT, MAX_PRSERVE_RECORD


class mongoDB():

    """
    Connect to mongoDB Server with provided ip:port, and map every provided API to specific db collection.
    The schema for insertion API is defined in ./insert_schema.json, which would be used to check type correctness of given data.
    """
    def __init__(self):
        self.client = pymongo.MongoClient(f"mongodb://{IP}:{PORT}/")

        with open("./insert_schema.json", "r") as f:
            self.insert_schema = json.load(f)   
        self.factory_list = ["竹", "中", "南"]
        self.mapper = {
            self.insertEarthquake.__name__:"earthquake",
            self.insertElectricity.__name__:"electricity",
            self.insertReservoir.__name__:"reservoir"
        }
        self.db = self.client["meteorological_center"]
        self.db['earthquake'].create_index("time")
        self.db['reservoir'].create_index("time")
        self.db['electricity'].create_index("time")
        self.db['factory'].create_index("time")


    # If given data dictionary has some value that is marked as NULL, remove key:value from data
    def filter_anomaly(self, data):
        t = {}
        for key, value in data.items():
            if value == -1.0 or value == "-":
                continue
            else:
                t[key]=value
        return t

    # Check the value type of input dictionary data based on input_schema,
    # return false if unmatched data type is detected, or raise KeyError if key is missed
    def __data_valid(self, data, functName):
        insert_schema_table = None
        for collection_schema in self.insert_schema:
            if(collection_schema['collection_name'] == self.mapper[functName]):
                insert_schema_table = collection_schema['schema']
                break
            
        for var, _type in insert_schema_table.items():
            if type(data[var]) != eval(_type):
                if eval(_type) == float:
                    if type(data[var]) != int:
                        return False
                else:
                    return False
        return True

    # insert earthquake data into DB
    def __process_an_insert_earth_quake(self, data):
        if type(data['time']) == str: 
            data['time'] = datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
        assert self.__data_valid(data, self.insertEarthquake.__name__) == True
        data = self.filter_anomaly(data)
        magnitude = data.pop('magnitude')
        self.db['earthquake'].insert_one(data)
        factories = self.db['factory'].find()

        # Organize the structure of data to fit 'factory' collection, and then update the document
        for data_fac in magnitude:
            factory_data = {key: value for key, value in data.items()}
            factory_data['factory'] = data_fac['factory']
            factory_data['magnitude'] = data_fac['magnitude']
            del factory_data['_id']
            print(factory_data)
            self.db['factory'].insert_one(factory_data)



    # check if any elements in given data list is already exist in the DB. If so, remove redundant records from input data list.
    # Caution: This method is only work for insert_earth_quake 
    def __filter_redundancy_data(self, datas):
        info=[]
        for i in datas:
            d = {key: value for key, value in i.items() if key != "magnitude"}
            if type(d['time']) == str:
                d['time'] = datetime.strptime(d['time'], "%Y-%m-%d %H:%M:%S")
            info.append( d )
        db_data = list(self.retrieveEarthquake(quantity = len(datas)))
        datas = [j for i, j in zip(info, datas) if i not in db_data]
        return datas


    def insertEarthquake(self, data):
        # the input of data may contain many records (list type) or only contain one record (dict type)
        if(type(data) == list):
            data = self.__filter_redundancy_data(data)
            for d in data:
                self.__process_an_insert_earth_quake(d)
        else:
            self.__process_an_insert_earth_quake(data)

        return 0

    def insertReservoir(self, data):
        data['time'] = datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
        assert self.__data_valid(data, self.insertReservoir.__name__) == True
        data = self.filter_anomaly(data)
        try:
            name = data.pop("name")
        except KeyError as e:
            print(f"Insertion failed. Reservoir name is not provided or is anomoly (-).\n data = {data}")
            return
        if len(list(self.db['reservoir'].find({"name":name}))) == 0:
            self.db['reservoir'].insert_one(
                {
                    "name":name,
                    "data":[]
                }
            )

        # Add a new record into assigned reservoir name 
        self.db['reservoir'].update_one(
            {"name":name},
            { "$push":{"data":data}}
        )

        return 0

    def insertElectricity(self, data):
        data['time'] = datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
        assert self.__data_valid(data, self.insertElectricity.__name__) == True
        data = self.filter_anomaly(data)
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
        ret = self.db['earthquake'].find({},{"_id":0}).sort("time", -1).limit(min(quantity, MAX_PRSERVE_RECORD))
        ret = [x for x in ret]
        # If no matched data exist in the db
        if len(ret,) == 0:
            ret = []
            ret.append({'time': None, 'M_L': -1.0, 'focal_dep': -1.0, 'longitude': -1.0, 'latitude': -1.0})
        return ret


# {'time': datetime.datetime(2023, 5, 12, 3, 40, 52), 'M_L': 3.6, 'focal_dep': 3.2, 'longitude': 41.0,
# 'latitude':20.7, 'factory': '南', 'magnitude': 0.0003714193582435097}

    def retrieveFactoryEarthquake(self, quantity=1, factory=None):
        if factory == None:
            raise Exception("factory is not specified.")
        if factory not in self.factory_list:
            raise Exception(f"Invalid factory's name. It should be {self.factory_list}")
        if quantity>MAX_PRSERVE_RECORD:
            raise Exception("requested quantity exceed.")
        else:
            ret = self.db['factory'].find({"factory":factory},{"_id":0}).limit(min(quantity, MAX_PRSERVE_RECORD))
            
            ret = [x for x in ret]
            # If no matched data exist in the db
            if len(ret) == 0:
                ret = []
                ret.append({'time': None, 'M_L': -1, 'focal_dep': -1, 'longitude': -1, 'latitude': -1, 'magnitude': -1})
        return ret

    def retrieveElectricity(self, quantity=1, region=None):
        if region == None:
            raise Exception("region not specified.")
            
        if quantity>MAX_PRSERVE_RECORD:
            raise Exception("requested quantity exceed.")

        ret = self.db['electricity'].find({"region":region},{"data":1, "_id":0}).limit(min(quantity, MAX_PRSERVE_RECORD))
        ret = [x['data'] for x in ret][0]
        # If no matched data exist in the db
        if(len(ret) == 0):
            ret = []
            ret.append({'power_usage': -1.0, 'power_generate': -1.0, 'time': None})
        return ret

    def retrieveReservoir(self, quantity=1, name=None):
        if name == None:
            raise Exception("reservoir not specified.")
        if quantity>MAX_PRSERVE_RECORD:
            raise Exception("requested quantity exceed.")
        ret = self.db['reservoir'].find({"name":name},{"data":1, "_id":0}).sort("time", -1).limit(min(quantity, MAX_PRSERVE_RECORD))
        ret = [x['data'] for x in ret]
        # If no matched data exist in the db
        if(len(ret) == 0):
            ret = []
            ret.append({'time':None, 'percentage': -1.0, 'water_supply': -1.0, 'name': name})
        return ret

    # Delete all datas of assigned DB in MongoDB server, proceed with caution!
    def reset(self):
        collection = self.db["earthquake"]
        result = collection.delete_many({})
        collection = self.db["electricity"]
        result = collection.delete_many({})
        collection = self.db["reservoir"]
        result = collection.delete_many({})
        collection = self.db["factory"]
        result = collection.delete_many({})