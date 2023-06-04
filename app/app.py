from flask import Flask, render_template, jsonify, request, send_from_directory
from dbAPI.MongoDB import MongoDB
from datetime import datetime

app = Flask(__name__)
app.debug = True

#-------------------------       frontend       -------------------------#

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route('/toggle_menu', methods=['GET'])
def toggle_menu():
    menu_state = request.args.get('menu_state')
    menu_links_state = request.args.get('menu_links_state')

    print("click toggle_menu !")

    return jsonify({'message': 'Menu toggled successfully'})


# 初始化電力、水量和地震資訊的變量

# 竹(石門水庫、寶山第二水庫、永和山水庫)
hsinchu_data = {
    "electricity_value": 2000, "electricity_maximum": 3000,
    "earthquake_time": "2022/5/23 下午 6:23:00", "earthquake_magnitude": "1",
    "reservoir_name_1": "石門水庫", "reservoir_percentage_1": f"{40}%", "reservoir_time_1": f"最後更新時間: 1990-01-01",
    "reservoir_name_2": "寶山第二水庫", "reservoir_percentage_2": f"{60}%", "reservoir_time_2": f"最後更新時間: 1990-01-01",
    "reservoir_name_3": "永和山水庫", "reservoir_percentage_3": f"{80}%", "reservoir_time_3": f"最後更新時間: 1990-01-01",
}

# 中(鯉魚潭水庫、德基水庫)
taichung_data = {
    "electricity_value": 1000, "electricity_maximum": 2000,
    "earthquake_time": "2022/5/24 下午 6:24:00", "earthquake_magnitude": "2", 
    "reservoir_name_1": "鯉魚潭水庫", "reservoir_percentage_1": f"{10}%", "reservoir_time_1": f"最後更新時間: 1990-01-01",
    "reservoir_name_2": "德基水庫", "reservoir_percentage_2": f"{20}%", "reservoir_time_2": f"最後更新時間: 1990-01-01",
    "reservoir_name_3": "", "reservoir_percentage_3": f"{30}%", "reservoir_time_3": f"最後更新時間: 1990-01-01",
}

# 南(南化水庫、曾文水庫、烏山頭水庫)
tainan_data = {
    "electricity_value": 500, "electricity_maximum": 1000,
    "earthquake_time": "2022/5/25 下午 6:25:00", "earthquake_magnitude": "3",
    "reservoir_name_1": "南化水庫", "reservoir_percentage_1": f"{1}%", "reservoir_time_1": f"最後更新時間: 1990-01-01",
    "reservoir_name_2": "曾文水庫", "reservoir_percentage_2": f"{2}%", "reservoir_time_2": f"最後更新時間: 1990-01-01",
    "reservoir_name_3": "烏山頭水庫", "reservoir_percentage_3": f"{3}%", "reservoir_time_3": f"最後更新時間: 1990-01-01",
}

factory_list = ["hsinchu", "taichung", "tainan"]

all_data = {
    "hsinchu": hsinchu_data,
    "taichung": taichung_data,
    "tainan": tainan_data
}

# Mapping factory to reservoir, earthquake, electricity 
reservoir_list = {
    "hsinchu": ("石門水庫", "寶山第二水庫", "永和山水庫"),
    "taichung": ("鯉魚潭水庫", "德基水庫"),
    "tainan": ("南化水庫", "曾文水庫", "烏山頭水庫")
}

earthquake_mapping = {
    "hsinchu": "竹",
    "taichung": "中",
    "tainan": "南",
}

electricity_mapping = {
    "hsinchu": "北",
    "taichung": "中",
    "tainan": "南",
}


def get_factory_data(factory: str, all_data: dict):
    print(f"[Backend] Click {factory} !")
    if factory not in factory_list:
        print(f"[Backend] Factory {factory} not found !")
        return jsonify({'message': 'Factory not found'}), 404
    
    # earthquake
    print(earthquake_mapping.get(factory))
    earthquake_query = db.retrieve_earthquake_data_by_factory(factory=earthquake_mapping.get(factory), quantity=1)[0]
    print(earthquake_query)
    all_data.get(factory)["earthquake_time"] = earthquake_query["time"]
    all_data.get(factory)["earthquake_magnitude"] = earthquake_query["magnitude"]
    
    # electricity
    print(electricity_mapping.get(factory))
    electricity_query = db.retrieve_electricity_data_by_region(region=electricity_mapping.get(factory), quantity=1,)[0]
    print(electricity_query)
    all_data.get(factory)["electricity_value"] = electricity_query["power_usage"]
    all_data.get(factory)["electricity_maximum"] = electricity_query["power_generate"]
    
    # reservoir
    for i, reservoir in enumerate(reservoir_list.get(factory), start=1):
        reservoir_query = db.retrieve_reservoir_data_by_name(name=reservoir, quantity=3)[0]
        print(reservoir_query)
        all_data.get(factory)[f"reservoir_percentage_{i}"] = reservoir_query["percentage"]
        all_data.get(factory)[f"reservoir_time_{i}"] = reservoir_query["time"]
    if(factory == "taichung"):
        all_data.get(factory)["reservoir_name_3"] = ""
        all_data.get(factory)[f"reservoir_percentage_3"] = ""
        all_data.get(factory)["reservoir_time_3"] = ""

    
@app.route('/hsinchu', methods=['GET'])
def hsinchu():
    get_factory_data(factory="hsinchu", all_data=all_data), 200
    return jsonify({'data': all_data.get("hsinchu")})


@app.route('/taichung', methods=['GET'])
def taichung():
    get_factory_data(factory="taichung", all_data=all_data), 200
    return jsonify({'data': all_data.get("taichung")})


@app.route('/tainan', methods=['GET'])
def tainan():
    get_factory_data(factory="tainan", all_data=all_data), 200
    return jsonify({'data': all_data.get("tainan")})


#-------------------------       database       -------------------------#

db = MongoDB()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)