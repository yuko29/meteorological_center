import requests
import re
import math
from math import sin, cos, radians
from datetime import datetime,timezone,timedelta
from dbAPI.MongoDB import MongoDB

def get_now_time():
    dtUTC = datetime.utcnow().replace(tzinfo = timezone.utc) #UTC
    dtUTC_8 = dtUTC.astimezone(timezone(timedelta(hours = 8))) #UTC+8
    now_time = dtUTC_8.strftime("%Y-%m-%d %H:%M:%S")
    
    return now_time

def get_history(url: str):
    
    try:
        earthquake = requests.get(url) 
    except requests.exceptions.RequestException as e:
        print("[crawling] ", e)
        print("[crawling]  Quit crawling...")
        exit()
    
    html_content = earthquake.content.decode('utf-8')

    pattern = re.compile(r'var\s+locations\s*=\s*([^;]+);') # format of "var location"
    matches = pattern.findall(html_content) # find content in html that matches format
    history = eval(matches[0]) # split to a list
    
    return history

def crawl_data(url: str):
    
    history = get_history(url)
    format_time = datetime.strptime(history[0][2], "%Y-%m-%d %H:%M:%S")
    print("format_time: ", format_time)
    history = {'time':format_time, 'M_L':history[0][3], 'focal_dep': history[0][4], 'longitude': float(history[0][7]), 'latitude': float(history[0][8])}
    print("[crawling]  Crawled data: ", history)

    return history
    
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


def calculate_magnitude(data: dict, GG_factory: list):
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
        if PGA > 80:
            # PGV
            if PGV < 30:
                fac_magnitude.append( {"factory": fac['factory'], "magnitude": 5.0})
            elif PGV < 50:
                fac_magnitude.append( {"factory": fac['factory'], "magnitude": 5.5})
            elif PGV < 80:
                fac_magnitude.append( {"factory": fac['factory'], "magnitude": 6.0})
            elif PGV < 140:
                fac_magnitude.append( {"factory": fac['factory'], "magnitude": 6.5})
            else:
                fac_magnitude.append( {"factory": fac['factory'], "magnitude": 7.0})
        else:
            # PGA
            if PGA < 0.2:
                fac_magnitude.append( {"factory": fac['factory'], "magnitude": 0.0})
            elif PGA < 0.7:
                fac_magnitude.append( {"factory": fac['factory'], "magnitude": 1.0})
            elif PGA < 1.9:
                fac_magnitude.append( {"factory": fac['factory'], "magnitude": 2.0})
            elif PGA < 5.7:
                fac_magnitude.append( {"factory": fac['factory'], "magnitude": 3.0})
            else:
                fac_magnitude.append( {"factory": fac['factory'], "magnitude": 4.0})

    data['magnitude'] = fac_magnitude
    return(data)

def insert_to_db(time: str, M_L: float, focal_dep: float, longitude: float, latitude: float, magnitude_chu: float, magnitude_center: float, magnitude_south: float):
    a = MongoDB()
    #a = MongoDB(ip = "172.27.0.1", port = 27017)
  
    try:
        a.insert_earthquake_data({'time': time, 'M_L': M_L, 'focal_dep': focal_dep, 'longitude': longitude, 'latitude': latitude, 'magnitude': [{'factory': '竹', 'magnitude': magnitude_chu}, {'factory': '中', 'magnitude': magnitude_center}, {'factory': '南', 'magnitude': magnitude_south}]})
        print("[crawling]  Insert data: ", {'time': time, 'M_L': M_L, 'focal_dep': focal_dep, 'longitude': longitude, 'latitude': latitude, 'magnitude': [{'factory': '竹', 'magnitude': magnitude_chu}, {'factory': '中', 'magnitude': magnitude_center}, {'factory': '南', 'magnitude': magnitude_south}]})
    except:
        print("[crawling]  Insert data failed")
    
    # print(f"\n\n\nRETRIEVING EARTHQUAKE FOR FACTORY...\n\n")
    # for i in a.retrieve_earthquake_data_by_factory(factory = "竹", quantity = 10):
    #     print(i)
    #     print(type(i['time']))
    
    return

def main():
    url = "https://scweb.cwb.gov.tw/"
    GG_factory = [
    {'factory': '竹', 'longitude': 121.01, 'latitude': 24.773, 'Si': 1.758, 'Padj': 1.0, 'magnitude': []},
    {'factory': '中', 'longitude': 120.618, 'latitude': 24.2115, 'Si': 1.063, 'Padj': 1.0, 'magnitude': []},
    {'factory': '南', 'longitude': 120.272, 'latitude': 23.1135, 'Si': 1.968, 'Padj': 1.0, 'magnitude': []}
    ]
    
    now_time = get_now_time()
    print("------------------")
    print("[crawling]  Start crawling water, time:", now_time)
    
    earthQuake = crawl_data(url)
    earthQuake = calculate_magnitude(earthQuake, GG_factory)
    

    insert_to_db(earthQuake['time'], earthQuake['M_L'], earthQuake['focal_dep'], earthQuake['longitude'] \
    , earthQuake['latitude'], earthQuake['magnitude'][0]["magnitude"], earthQuake['magnitude'][1]["magnitude"] \
    , earthQuake['magnitude'][2]["magnitude"])
    
    
if __name__ == "__main__":
    main()