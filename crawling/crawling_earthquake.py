import requests
import re
import math
from math import sin, cos, radians
from dbAPI.MongoDB import MongoDB


def crawl_data_ten():
    earthquake = requests.get("https://scweb.cwb.gov.tw/") #將此頁面的HTML GET下來
    html_content = earthquake.content.decode('utf-8')

    pattern = re.compile(r'var\s+locations\s*=\s*([^;]+);')
    matches = pattern.findall(html_content)
    history = eval(matches[0])

    history_list = []
    for i in range(10):
        history_list.append({'time':history[i][2], 'M_L':history[i][3], 'focal_dep': history[i][4], 'longitude': float(history[i][7]), 'latitude': float(history[i][8])})
        #history_q.put({'time':history[0][2], 'M_L':history[0][3], 'focal_dep': history[0][4], 'longitude': float(history[0][7]), 'latitude': float(history[0][8])})

    return history_list


def crawl_data():
    earthquake = requests.get("https://scweb.cwb.gov.tw/") #將此頁面的HTML GET下來
    #print(earthquake.text) #印出HTML
    html_content = earthquake.content.decode('utf-8')

    pattern = re.compile(r'var\s+locations\s*=\s*([^;]+);')
    matches = pattern.findall(html_content)
    history = eval(matches[0])

    earthQuake = {'time':history[0][2], 'M_L':history[0][3], 'focal_dep': history[0][4], 'longitude': float(history[0][7]), 'latitude': float(history[0][8])}
    return earthQuake
    #earthEqake_test = {'time':"2023-5-12 03:40:52", 'M_L':3.6, 'focal_dep': 3.2, 'longitude': 41.0, 'latitude': 20.7}

def longitude_difference_to_km(longitude1, longitude2):
    """
    Convert the difference between two longitudes into kilometers using the haversine formula.
    
    Args:
        longitude1 (float): First longitude.
        longitude2 (float): Second longitude.
    
    Returns:
        float: The difference between the longitudes in kilometers.
    """
    earth_radius_km = 6371.0  # Earth's radius in kilometers
    
    # Convert the longitudes from degrees to radians
    lon1 = math.radians(longitude1)
    lon2 = math.radians(longitude2)
    
    # Calculate the difference between the longitudes in radians
    delta_lon = lon2 - lon1
    
    # Apply the haversine formula to calculate the angular distance
    a = math.sin(delta_lon / 2) ** 2
    c = 2 * math.sin(a)
    distance = earth_radius_km * c
    
    return abs(distance)


def latitude_difference_to_km(latitude1, latitude2):
    """
    Convert the difference between two latitudes into kilometers.
    
    Args:
        latitude1 (float): First latitude.
        latitude2 (float): Second latitude.
    
    Returns:
        float: The difference between the latitudes in kilometers.
    """
    earth_radius_km = 6371.0  # Earth's radius in kilometers
    
    # Convert the latitudes from degrees to radians
    lat1 = radians(latitude1)
    lat2 = radians(latitude2)
    
    # Calculate the difference between the latitudes in radians
    delta_lat = lat2 - lat1
    
    # Calculate the distance using the arc length formula
    distance = earth_radius_km * delta_lat
    
    return abs(distance)

def getDistance(x, y):
    return math.sqrt(x**2 + y**2)

GG_factory = [
    {'factory': '竹', 'longitude': 121.01, 'latitude': 24.773, 'Si': 1.758, 'Padj': 1.0, 'magnitude': []},
    {'factory': '中', 'longitude': 120.618, 'latitude': 24.2115, 'Si': 1.063, 'Padj': 1.0, 'magnitude': []},
    {'factory': '南', 'longitude': 120.272, 'latitude': 23.1135, 'Si': 1.968, 'Padj': 1.0, 'magnitude': []}
]

def calculate_magnitude(data):
    fac_magnitude = []
    for fac in GG_factory:
        long_km = latitude_difference_to_km(fac['longitude'], data['longitude'])
        lati_km = latitude_difference_to_km(fac['latitude'], data['latitude'])
        r = getDistance( getDistance(long_km, lati_km), data['focal_dep'])

        longitude = fac['longitude']
        latitude = fac['latitude']
        si = fac['Si']
        padj = fac['Padj']
        PGA = 1.657*math.exp(1.533*data['M_L'])*( r **(-1.607))*fac['Si']*fac['Padj']
        PGV = PGA/8.6561
        if PGA>80:
            #print(PGV)
            fac_magnitude.append( {"factory":fac['factory'], "magnitude":PGV})
        else:
            #print(PGA)
            fac_magnitude.append({"factory":fac['factory'], "magnitude":PGA})

    data['magnitude'] = fac_magnitude
    return(data)

def get_new_update():
    crawled = crawl_data()
    eq_with_mag = calculate_magnitude(crawled)



earthQuake_list = crawl_data_ten()
for earthQuake in earthQuake_list:
    earthQuake = calculate_magnitude(earthQuake)
a = MongoDB()
#a.insert_earthquake_data(earthEqake_list)
#a.insert_earthquake_data(earthQuake_list[0])
a.insert_earthquake_data(earthQuake_list)

#{'time': '2023-5-12 03:40:52', 'M_L': 3.6, 'focal_dep': 3.2, 'longitude': 41.0, 'latitude': 20.7, 'magnitude': [{'factory': '竹', 'magnitude': 0.00032644588703523386}, {'factory': '中', 'magnitude': 0.00019905740360289052}, {'factory': '南', 'magnitude': 0.0003714193582435097}]}

#print(earthQuake_list)
