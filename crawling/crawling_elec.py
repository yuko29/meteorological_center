import requests
import re
from dbAPI.MongoDB import MongoDB

elec = requests.get("https://www.taiwanstat.com/powers/latest/") #將此頁面的HTML GET下來
#print(elec.text) #印出HTML
update_time = str(elec.json()["regionData"]["updateTime"])
update_time = update_time + ":00"
#print(update_time)
northSupply = float(elec.json()["regionData"]["northSupply"])   #北部即時發電量
southSupply = float(elec.json()["regionData"]["southSupply"])   #南部即時發電量
centerSupply = float(elec.json()["regionData"]["centerSupply"]) #中部即時發電量

northUsage = float(elec.json()["regionData"]["northUsage"])   #北部即時用電量
southUsage = float(elec.json()["regionData"]["southUsage"])   #南部即時用電量
centerUsage = float(elec.json()["regionData"]["centerUsage"]) #中部即時用電量

a = MongoDB()

Electricity_north = {'region':"北", 'power_usage':northUsage, 'power_generate': northSupply, 'time': update_time}
Electricity_center = {'region':"中", 'power_usage':centerUsage, 'power_generate': centerSupply, 'time': update_time}
Electricity_south = {'region':"南", 'power_usage':southUsage, 'power_generate': southSupply, 'time': update_time}

a.insert_electricity_data(Electricity_north)
a.insert_electricity_data(Electricity_center)
a.insert_electricity_data(Electricity_south)

print(Electricity_north)
print(Electricity_center)
print(Electricity_south)
#electricity_test = {'region':"北", 'power_usage':512.3, 'power_generate': 482.1, 'time': "2023-5-12 03:40:52"}


#print(Electricity)
