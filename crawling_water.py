from bs4 import BeautifulSoup
import requests
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

water = requests.get("https://fhy.wra.gov.tw/ReservoirPage_2011/Statistics.aspx") #將此頁面的HTML GET下來
#print(water.text) #印出HTML
soup = BeautifulSoup(water.text, 'html.parser')

reservoir = {}
re_list = ["石門水庫", "寶山第二水庫", "永和山水庫", "鯉魚潭水庫", "德基水庫", "南化水庫", "曾文水庫", "烏山頭水庫"]
for re in re_list:
    stw = soup.find('a', string = re).find_parent().find_parent().find_all("td")
    #print(re)
    
    if stw[1].string == "--":
        water_time = '-'
    else:
        water_time = str(stw[1].string)
    #print("水情時間: ", water_time) # 水情時間
    
    if stw[6].string == "--":
        water_avail = -1
    else:
        water_avail = locale.atof(stw[6].string)
    #print("有效蓄水量: ", water_avail) # 有效蓄水量
    
    if stw[7].string == "--":
        water_per = -1
    else:
        water_per = str(stw[7].string).replace(" %","")
        water_per = float(water_per)
    #print("蓄水百分比: ", water_per) # 蓄水百分比
    
    reservoir[re] = {"water_time": water_time, "water_avail": water_avail, "water_per": water_per}

    #print()

print(reservoir)