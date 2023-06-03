from bs4 import BeautifulSoup
import requests
from dbAPI.MongoDB import MongoDB

def get_water(url: str):
    try:
        water = requests.get(url) #將此頁面的HTML GET下來
    except requests.exceptions.RequestException:
        exit()
    soup = BeautifulSoup(water.text, 'html.parser')
    return soup

def handle_data(soup, re_list: list[str]):
    reservoir = {} # key: reservoir name, value: a dict of information
    
    for re in re_list:
        stw = soup.find('a', string = re).find_parent().find_parent().find_all("td")
        
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
    
    return reservoir

def insert_to_db(reservoir: dict, re_list: list[str]):
    a = MongoDB()
    for re in re_list:
        a.insert_reservoir_data({'time':reservoir[re]['time'], 'percentage': reservoir[re]['percentage'], 'water_supply': reservoir[re]['volume'], 'name': re})
        #print(re, reservoir[re])

def main():
    url = "https://fhy.wra.gov.tw/ReservoirPage_2011/Statistics.aspx"
    re_list = ["石門水庫", "寶山第二水庫", "永和山水庫", "鯉魚潭水庫", "德基水庫", "南化水庫", "曾文水庫", "烏山頭水庫"]
    
    soup = get_water(url)
    reservoir = handle_data(soup, re_list)
    insert_to_db(reservoir, re_list)
    
if __name__ == "__main__":
    main()


