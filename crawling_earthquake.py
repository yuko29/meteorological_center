import requests
import re

earthquake = requests.get("https://scweb.cwb.gov.tw/") #將此頁面的HTML GET下來
#print(earthquake.text) #印出HTML

html_content = earthquake.content.decode('utf-8')

pattern = re.compile(r'var\s+locations\s*=\s*([^;]+);')
matches = pattern.findall(html_content)
history = eval(matches[0])
print(history)
print()
print("最近一次地震")
print("時間: ", history[0][2])
print("規模: ", history[0][3])
print("地震深度: ", history[0][4])
print("東經: ", history[0][7])
print("北緯: ", history[0][8])