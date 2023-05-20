import json


        self.earthEqake = self.db['earthQuake_latest']
        self.reservoir = self.db['reservoir']
        self.electricity = self.db['electricity']

out = []
collections = ['earthquake', 'reservoir', 'electricity']
schema = [
    {
        'collection_name': 'earthquake', 
        'time': "str", 
        'focal_del': "float", 
        'longitude': "float",
        'latitude': "float",
    },
    {
        'collection_name':'reservoir',
        'time': "str",
        'water_supply': "float",
        'percentage': "float",
    },
    {
        'collection_name':'electricity',
        'region':"str",
        'power_usage':"float",
        'power_generate':"float",
        'time':"str",
    }

        
        if(functName == self.insertElectricity.__name__):
            return type(data['region']) == str\
                    and type(data['power_usage']) == float\
                    and type(data['power_generate']) == float\
                    and type(data['time']) == str
        
]


 
 
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
