from bs4 import BeautifulSoup
import requests
import locale
from dbAPI.MongoDB import MongoDB

water = requests.get("https://fhy.wra.gov.tw/ReservoirPage_2011/Statistics.aspx") #將此頁面的HTML GET下來
#print(water.text) #印出HTML
soup = BeautifulSoup(water.text, 'html.parser')

reservoir = {}
a = MongoDB()
re_list = ["石門水庫", "寶山第二水庫", "永和山水庫", "鯉魚潭水庫", "德基水庫", "南化水庫", "曾文水庫", "烏山頭水庫"]
for re in re_list:
    stw = soup.find('a', string = re).find_parent().find_parent().find_all("td")
    #print(re)
    
    if stw[1].string == "--":
        water_time = '-'
    else:
        water_time = str(stw[1].string)
    
    if stw[6].string == "--":
        water_avail = -1.0
    else:
        water_avail = float(stw[6].string.replace(',',''))
    
    if stw[7].string == "--":
        water_per = -1.0
    else:
        water_per = str(stw[7].string).replace(" %","")
        water_per = float(water_per)
    
    reservoir[re] = {"time": water_time, "volume": water_avail, "percentage": water_per}
    a.insert_reservoir_data({'time':water_time, 'percentage': water_per, 'water_supply': water_avail, 'name': re})


print(reservoir)
print("---------------------------")
data = a.retrieve_reservoir_data_by_name(quantity = 1, name="曾文水庫")
print(data)

#reservoir_test2 = {'time':"2023-5-12 03:40:52", 'percentage': 42.6, 'water_supply': 321.2, 'name': "德基水庫"}