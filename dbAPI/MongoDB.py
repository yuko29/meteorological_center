import pymongo
import bson
from dbAPI.Database import Database
from strongtyping.strong_typing import match_class_typing
from typing import Optional, List, Dict, Union, Any, Tuple
from datetime import datetime
import pprint
from dbAPI.db_config import IP, PORT, MAX_PRSERVE_RECORD, COLLECTION_LIST

@match_class_typing
class MongoDB(Database):
    
    def __init__(self, ip: Optional[str] = None, port: Optional[int]=None, db_name: Optional[str] = "my_mongoDB", collection_list:  Optional[list] = None):
        if ip == None or port == None:
            print("[MongoDB] None ip or port specified. Loading db_config")
            ip = IP
            port = PORT
        super().__init__(ip=ip, port=port, db_name=db_name)
        self.collection_list = collection_list
        if self.collection_list == None:
            print("[MongoDB] None collection_list specified. Loading db_config")
            self.collection_list = COLLECTION_LIST

        for collection in self.collection_list:
            self.db[collection].create_index("time")
        self.anomaly_values = {str:"-", float:-1.0, datetime:None, list:None, int:-1}
    
    
    def __filter_anomaly(self, data: dict):  # Filter out the data bad values, rules are defined in self.anomaly_values
        for key, value in list(data.items()):
            assert type(value) != bson.objectid.ObjectId, "[MongoDB] Insertion of two same data instances detected!\n \
If you're sure you are right, delete \"_id\" in your input data."
            if(self.anomaly_values[type(value)] == value):
                data.pop(key)


    # This function checks and filte all 
    def __delete_earthquake_duplicate(self, data: List[Dict], collection: str):
        latest_data = [x for x in self.retrieve_data(collection_name="earthquake", condition={}, sort=("time", -1), limit=len(data))]
        filtered_data = []
        for input, db in zip(data, latest_data):
            magnitude = input.pop("magnitude")  # organize the structure of input data so their format is same
            if input != db:
                input['magnitude'] = magnitude  # restore the format of input data
                filtered_data.append(input)
                print(input)
                print(db)
    
        return filtered_data

    @staticmethod
    def __transfer_time_type(data):
        assert not (data.get("time") is None), "[MongoDB] Time is not provided in given data"
        if(type(data['time'])==str):
            data['time'] = datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
        return data

    def __insert_into_factory_and_earthqake(self, single_data: Dict):
        self.__filter_anomaly(single_data)
        factory_data = single_data.pop('magnitude')
        self.insert_data("earthquake", single_data)
        for factory in factory_data:
            del single_data['_id']  # insertion will assign "_id" key to insert data
            single_data['factory'] = factory['factory']
            single_data['magnitude'] = factory['magnitude']
            self.insert_data("factory", single_data)

    def insert_earthquake_data(self, data: Union[Dict, List[Dict]]):
        if(type(data) == list):    # input is a list of earthquake data 
            data = self.__delete_earthquake_duplicate(data, "earthquake")
            for x in data:
                x = self.__transfer_time_type(x)
                self.__insert_into_factory_and_earthqake(x)
        else:                      # input is a single earthquake data
            data = self.__transfer_time_type(data)
            self.__insert_into_factory_and_earthqake(data)
    
    
    def insert_electricity_data(self, data: dict):
        data = self.__transfer_time_type(data)
        assert not (data.get("region") is None), "[MongoDB] Region is not provided in electricity data"
        self.__filter_anomaly(data)
        self.insert_data("electricity", data)
        
    
    def insert_reservoir_data(self, data: dict):
        data = self.__transfer_time_type(data)
        assert not (data.get("name") is None), "[MongoDB] Reservoir name is not provided in reservoir data"
        self.__filter_anomaly(data)
        self.insert_data("reservoir", data)
        
    
    def retrieve_earthquake_data_by_factory(self, factory: str=None, quantity:int =1):  # factory_location = ["竹", "中", "南"]
        assert factory is not None, "[MongoDB] Fatory is not specified in given request"
        assert type(quantity) == int, "[MongoDB] Quantity must be integer"
        return [x for x in self.retrieve_data(
                collection_name="factory", condition={"factory": factory}, sort=('time', -1), limit=quantity)]

    def retrieve_earthquake_data(self, quantity:int =1):
        assert type(quantity) == int, "[MongoDB] Quantity must be integer"
        return [x for x in self.retrieve_data(
                collection_name="earthquake", condition={}, sort=('time', -1), limit=quantity)]
    
    def retrieve_reservoir_data_by_name(self, name: str=None, quantity:int =1):
        assert name is not None, "[MongoDB] Resovoir name is not specified in given request"
        assert type(quantity) == int, "[MongoDB] Quantity must be integer"
        return [x for x in self.retrieve_data(
                collection_name="reservoir", condition={"name": name}, sort=('time', -1), limit=quantity)]
    
    
    def retrieve_electricity_data_by_region(self, region: str=None, quantity:int =1):  # region = ["北", "中", "南"]
        assert type(quantity) == int, "[MongoDB] Quantity must be integer"
        assert region is not None, "[MongoDB] Region is not specified in given request"
        return [x for x in self.retrieve_data(
                collection_name="electricity", condition={"region": region}, sort=('time', 1), limit=quantity)]
    
    
    def print_all_data(self, collection: str):
        print(f"Collection: {collection}")
        for post in self.db[collection].find():
            pprint.pprint(post)   
        print("\n")
    
    
    def clean_collection(self, collection: str):
        self.db[collection].delete_many({})
        

    def reset(self):
        self.clean_all_collection()

    def clean_all_collection(self):
        if self.collection_list is not None:
            for collection in self.collection_list:
                self.clean_collection(collection)
                