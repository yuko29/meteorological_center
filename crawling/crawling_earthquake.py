import requests
import re
import math
from math import sin, cos, radians
from dbAPI.MongoDB import MongoDB


def get_history(url: str):
    
    try:
        earthquake = requests.get(url) 
    except requests.exceptions.RequestException:
        exit()
    
    html_content = earthquake.content.decode('utf-8')

    pattern = re.compile(r'var\s+locations\s*=\s*([^;]+);') # format of "var location"
    matches = pattern.findall(html_content) # find content in html that matches format
    history = eval(matches[0]) # split to a list
    
    return history

def crawl_ten_data(url: str):
    history = get_history(url)
    history_list = []
    for i in range(10):
        history_list.append({'time':history[i][2], 'M_L':history[i][3], 'focal_dep': history[i][4], 'longitude': float(history[i][7]), 'latitude': float(history[i][8])})
        #history_q.put({'time':history[0][2], 'M_L':history[0][3], 'focal_dep': history[0][4], 'longitude': float(history[0][7]), 'latitude': float(history[0][8])})

    return history_list


def crawl_data(url: str):
    history = get_history(url)
    earthQuake = {'time':history[0][2], 'M_L':history[0][3], 'focal_dep': history[0][4], 'longitude': float(history[0][7]), 'latitude': float(history[0][8])}
    return earthQuake
    
def longitude_difference_to_km(longitude1: float, longitude2: float):
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


def latitude_difference_to_km(latitude1: float, latitude2: float):
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

def getDistance(x: float, y: float):
    return math.sqrt(x**2 + y**2)


def calculate_magnitude(data: dict, GG_factory: list[dict]):
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

def get_new_update(url: str):
    crawled = crawl_data(url)
    eq_with_mag = calculate_magnitude(crawled)

def main():
    url = "https://scweb.cwb.gov.tw/"
    GG_factory = [
    {'factory': '竹', 'longitude': 121.01, 'latitude': 24.773, 'Si': 1.758, 'Padj': 1.0, 'magnitude': []},
    {'factory': '中', 'longitude': 120.618, 'latitude': 24.2115, 'Si': 1.063, 'Padj': 1.0, 'magnitude': []},
    {'factory': '南', 'longitude': 120.272, 'latitude': 23.1135, 'Si': 1.968, 'Padj': 1.0, 'magnitude': []}
    ]
    
    earthQuake_list = crawl_ten_data(url)

    for earthQuake in earthQuake_list:
        earthQuake = calculate_magnitude(earthQuake, GG_factory)
    #print(earthQuake_list)
    
    a = MongoDB()
    a.insert_earthquake_data(earthQuake_list)


if __name__ == "__main__":
    main()