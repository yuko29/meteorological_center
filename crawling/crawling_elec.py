import requests
import re
#from dbAPI.MongoDB import MongoDB

def get_elec(url: str):
    try:
        elec = requests.get(url) #將此頁面的HTML GET下來
    except requests.exceptions.RequestException:
        exit()
    
    return elec

def handle_data(elec):
    
    update_time = str(elec.json()["regionData"]["updateTime"])
    update_time = update_time + ":00"
    

    northSupply = float(elec.json()["regionData"]["northSupply"])   #北部即時發電量
    southSupply = float(elec.json()["regionData"]["southSupply"])   #南部即時發電量
    centerSupply = float(elec.json()["regionData"]["centerSupply"]) #中部即時發電量
    Supply = [northSupply, southSupply, centerSupply]
    
    northUsage = float(elec.json()["regionData"]["northUsage"])   #北部即時用電量
    southUsage = float(elec.json()["regionData"]["southUsage"])   #南部即時用電量
    centerUsage = float(elec.json()["regionData"]["centerUsage"]) #中部即時用電量
    Usage = [northUsage, southUsage, centerUsage]

    return update_time, Supply, Usage

def insert_to_db(update_time:str, Supply: list[float], Usage: list[float]):
    
    Electricity_north = {'region':"北", 'power_usage': Usage[0], 'power_generate': Supply[0], 'time': update_time}
    Electricity_center = {'region':"中", 'power_usage': Usage[1], 'power_generate': Supply[1], 'time': update_time}
    Electricity_south = {'region':"南", 'power_usage': Usage[2], 'power_generate': Supply[2], 'time': update_time}
    
    #a = MongoDB()
    #a.insert_electricity_data(Electricity_north)
    #a.insert_electricity_data(Electricity_center)
    #a.insert_electricity_data(Electricity_south)
    
    #print(Electricity_north)
    #print(Electricity_center)
    #print(Electricity_south)

def main():
    url = "https://www.taiwanstat.com/powers/latest/"
    elec = get_elec(url)
    update_time, Supply, Usage = handle_data(elec)
    insert_to_db(update_time, Supply, Usage)
    
if __name__ == "__main__":
    main()

