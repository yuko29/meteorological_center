from bs4 import BeautifulSoup
import requests
from datetime import datetime,timezone,timedelta
from dbAPI.MongoDB import MongoDB

def get_water(url: str):
    try:
        water = requests.get(url) #將此頁面的HTML GET下來
    except requests.exceptions.RequestException as e:
        print("[crawling] ", e)
        print("[crawling]  Quit crawling...")
        exit()
    soup = BeautifulSoup(water.text, 'html.parser')
    return soup

def handle_data(a, soup, re_list: list):
    for re in re_list:
        stw = soup.find('a', string = re).find_parent().find_parent().find_all("td")
    
        if stw[1].string == "--":
            print("[crawling] ", re, " no data crawled")
            continue
        else:
            water_time = str(stw[1].string)
        
        if stw[6].string == "--":
            print("[crawling] ", re, " no data crawled")
            continue
        else:
            water_avail = float(stw[6].string.replace(',',''))
        
        if stw[7].string == "--":
            print("[crawling] ", re, " no data crawled")
            continue
        else:
            water_per = str(stw[7].string).replace(" %","")
            water_per = float(water_per)
        
        reservoir_data = {'name': re, "time": water_time, "water_supply": water_avail, "percentage": water_per}
        a.insert_reservoir_data(reservoir_data)
        
        print("[crawling] ", re, " insert data ", reservoir_data)
    return 

def main():
    url = "https://fhy.wra.gov.tw/ReservoirPage_2011/Statistics.aspx"
    re_list = ["石門水庫", "寶山第二水庫", "永和山水庫", "鯉魚潭水庫", "德基水庫", "南化水庫", "曾文水庫", "烏山頭水庫"]
    
    dtUTC = datetime.utcnow().replace(tzinfo = timezone.utc) #UTC
    dtUTC_8 = dtUTC.astimezone(timezone(timedelta(hours = 8))) #UTC+8
    now_time = dtUTC_8.strftime("%Y-%m-%d %H:%M:%S")
    print("------------------")
    print("[crawling]  Start crawling water, time:", now_time)

    soup = get_water(url)
    #a = MongoDB()
    a = MongoDB(ip = "172.27.0.1", port = 27017)
    handle_data(a, soup, re_list)
    
    print()
    print("Retrieve data")
    print(a.retrieve_reservoir_data_by_name(quantity= 50, name = "永和山水庫"))

    a.reset()
    
if __name__ == "__main__":
    main()


