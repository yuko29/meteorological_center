import requests
import re
from datetime import datetime,timezone,timedelta
from dbAPI.MongoDB import MongoDB

def get_now_time():
    dtUTC = datetime.utcnow().replace(tzinfo = timezone.utc) #UTC
    dtUTC_8 = dtUTC.astimezone(timezone(timedelta(hours = 8))) #UTC+8
    now_time = dtUTC_8.strftime("%Y-%m-%d %H:%M:%S")
    
    return now_time

def get_elec(url: str):
    try:
        elec = requests.get(url) #將此頁面的HTML GET下來
        print("[crawling]  Electricity crawled")
    except requests.exceptions.RequestException as e:
        print("[crawling] ", e)
        print("[crawling]  Quit crawling...")
        exit()
    
    return elec

def handle_data(elec):
    
    update_time = str(elec.json()["regionData"]["updateTime"])
    update_time = update_time + ":00"
    format_time = datetime.strptime(update_time, "%Y-%m-%d %H:%M:%S")
    
    northSupply = float(elec.json()["regionData"]["northSupply"])   #北部即時發電量
    southSupply = float(elec.json()["regionData"]["southSupply"])   #南部即時發電量
    centerSupply = float(elec.json()["regionData"]["centerSupply"]) #中部即時發電量
    Supply = [northSupply, southSupply, centerSupply]
    
    northUsage = float(elec.json()["regionData"]["northUsage"])   #北部即時用電量
    southUsage = float(elec.json()["regionData"]["southUsage"])   #南部即時用電量
    centerUsage = float(elec.json()["regionData"]["centerUsage"]) #中部即時用電量
    Usage = [northUsage, southUsage, centerUsage]

    return format_time, Supply, Usage

def insert_to_db(update_time: datetime, region: str, power_usage: float, power_generate: float):
    
    Electricity = {'region':region, 'power_usage': power_usage, 'power_generate': power_generate, 'time': update_time}
    
    #a = MongoDB(ip = "172.27.0.1", port = 27017)
    a = MongoDB()
    try:
        a.insert_electricity_data(Electricity)
        print("[crawling]  Insert data: ", Electricity)
    except:
        print("[crawling]  Insert data failed")

    # print(f"\nRETRIEVING ELECTRICITY...\n")
    # for i in a.retrieve_electricity_data_by_region(quantity= 50,region = region):
    #     print(i)
    # print()
    return

def main():
    url = "https://www.taiwanstat.com/powers/latest/"
    region_list = ['北', '中', '南']
    
    now_time = get_now_time()
    print("------------------")
    print("[crawling]  Start crawling electricity, time:", now_time)
    
    elec = get_elec(url)
    update_time, Supply, Usage = handle_data(elec)
    
    for i in range(3):
        insert_to_db(update_time, region_list[i], Supply[i], Usage[i])
    
    
if __name__ == "__main__":
    main()

