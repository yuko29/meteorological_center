import requests
import re

elec = requests.get("https://www.taiwanstat.com/powers/latest/") #將此頁面的HTML GET下來
#print(elec.text) #印出HTML

northSupply = elec.json()["regionData"]["northSupply"]   #北部即時發電量
eastSupply = elec.json()["regionData"]["eastSupply"]     #東部即時發電量
southSupply = elec.json()["regionData"]["southSupply"]   #南部即時發電量
centerSupply = elec.json()["regionData"]["centerSupply"] #中部即時發電量
print("北部即時發電量: " + northSupply + " 萬瓩")
print("東部即時發電量: " + eastSupply + " 萬瓩")
print("南部即時發電量: " + southSupply + " 萬瓩")
print("中部即時發電量: " + centerSupply+ " 萬瓩")
print()
northUsage = elec.json()["regionData"]["northUsage"]   #北部即時用電量
eastUsage = elec.json()["regionData"]["eastUsage"]     #東部即時用電量
southUsage = elec.json()["regionData"]["southUsage"]   #南部即時用電量
centerUsage = elec.json()["regionData"]["centerUsage"] #中部即時用電量
print("北部即時用電量: " + northUsage + " 萬瓩")
print("東部即時用電量: " + eastUsage + " 萬瓩")
print("南部即時用電量: " + southUsage + " 萬瓩")
print("中部即時用電量: " + centerUsage+ " 萬瓩")