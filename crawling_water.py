from bs4 import BeautifulSoup
import requests

water = requests.get("https://fhy.wra.gov.tw/ReservoirPage_2011/Statistics.aspx") #將此頁面的HTML GET下來
#print(water.text) #印出HTML

soup = BeautifulSoup(water.text, 'html.parser')
#title_tag = soup.title
re_list = ["石門水庫", "寶山第二水庫", "永和山水庫", "鯉魚潭水庫", "德基水庫", "南化水庫", "曾文水庫", "烏山頭水庫"]
for re in re_list:
    stw = soup.find('a', string = re).find_parent().find_parent().find_all("td")
    print(re)
    print("水情時間: " + stw[1].string) # 水情時間
    print("有效蓄水量: " + stw[6].string) # 有效蓄水量
    print("蓄水百分比: " + stw[7].string) # 蓄水百分比
    print()