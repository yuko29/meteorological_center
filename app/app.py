from flask import Flask, render_template, jsonify, request, send_from_directory
from dbAPI.MongoDB import MongoDB
from datetime import datetime
import logging

app = Flask(__name__)
app.debug = True

#-------------------------       frontend       -------------------------#

@app.route('/')
def index():
    warn_electricity = False
    warn_earthquake = True
    return render_template('index.html', warn_earthquake=warn_earthquake, warn_electricity=warn_electricity)

@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route('/toggle_menu', methods=['GET'])
def toggle_menu():
    menu_state = request.args.get('menu_state')
    menu_links_state = request.args.get('menu_links_state')

    logging.warning("click toggle_menu !")

    return jsonify({'message': 'Menu toggled successfully'})


# 初始化電力、水量和地震資訊的變量

# 竹(石門水庫、寶山第二水庫、永和山水庫)
hsinchu_data = {
    "electricity_value": "-", "electricity_maximum": "-",
    "earthquake_time": "19901990-01-01 AM 00:00", "earthquake_magnitude": "-",
    "reservoir_name_1": "石門水庫", "reservoir_percentage_1": "-%", "reservoir_time_1": f"最後更新時間: 1990-01-01 AM 00:00",
    "reservoir_name_2": "寶山第二水庫", "reservoir_percentage_2": "-%", "reservoir_time_2": f"最後更新時間: 1990-01-01 AM 00:00",
    "reservoir_name_3": "永和山水庫", "reservoir_percentage_3": "-%", "reservoir_time_3": f"最後更新時間: 1990-01-01 AM 00:00",
}

# 中(鯉魚潭水庫、德基水庫)
taichung_data = {
    "electricity_value": "-", "electricity_maximum": "-",
    "earthquake_time": "19901990-01-01 AM 00:00", "earthquake_magnitude": "-", 
    "reservoir_name_1": "鯉魚潭水庫", "reservoir_percentage_1": "-%", "reservoir_time_1": f"最後更新時間: 1990-01-01 AM 00:00",
    "reservoir_name_2": "德基水庫", "reservoir_percentage_2": "-%", "reservoir_time_2": f"最後更新時間: 1990-01-01 AM 00:00",
    "reservoir_name_3": "", "reservoir_percentage_3": "", "reservoir_time_3": "",
}

# 南(南化水庫、曾文水庫、烏山頭水庫)
tainan_data = {
    "electricity_value": "-", "electricity_maximum": "-",
    "earthquake_time": "1990-01-01 AM 00:00", "earthquake_magnitude": "-",
    "reservoir_name_1": "南化水庫", "reservoir_percentage_1": "-%", "reservoir_time_1": f"最後更新時間: 1990-01-01 AM 00:00",
    "reservoir_name_2": "曾文水庫", "reservoir_percentage_2": "-%", "reservoir_time_2": f"最後更新時間: 1990-01-01 AM 00:00",
    "reservoir_name_3": "烏山頭水庫", "reservoir_percentage_3": "-%", "reservoir_time_3": f"最後更新時間: 1990-01-01 AM 00:00",
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


def update_factory_data(factory: str, all_data: dict):    # Retrieve data from database and return a json(dict) to frontend
    logging.info(f"[Backend] Click {factory} !")
    
    if factory not in factory_list:
        logging.info(f"[Backend] update_factory_data(): Factory {factory} not found !")
        return jsonify({'message': 'Factory not found'}), 404
    
    try:    # earthquake
        earthquake_query = db.retrieve_earthquake_data_by_factory(factory=earthquake_mapping.get(factory), quantity=1)[0]
        logging.info(f"[Backend] Query Earthquake SUCESS: {earthquake_query}")
        all_data.get(factory)["earthquake_time"] = earthquake_query["time"].strftime("%Y/%m/%d %p %I:%M")
        all_data.get(factory)["earthquake_magnitude"] = earthquake_query["magnitude"]
    except:
        logging.warning(f"[Backend] Query Earthquake FAIL: {factory}")
        
    try:    # electricity
        electricity_query = db.retrieve_electricity_data_by_region(region=electricity_mapping.get(factory), quantity=1,)[0]
        logging.info(f"[Backend] Query Electricity SUCESS: {electricity_query}")
        all_data.get(factory)["electricity_value"] = electricity_query["power_usage"]
        all_data.get(factory)["electricity_maximum"] = electricity_query["power_generate"]
    except:
        logging.warning(f"[Backend] Query Electricity FAIL: {factory}")
    
    try:    # reservoir
        if(factory == "taichung"):  # Taichung only has 2 reservoirs
            all_data.get(factory)["reservoir_name_3"] = ""
            all_data.get(factory)[f"reservoir_percentage_3"] = ""
            all_data.get(factory)["reservoir_time_3"] = ""

        for i, reservoir in enumerate(reservoir_list.get(factory), start=1):
            reservoir_query = db.retrieve_reservoir_data_by_name(name=reservoir, quantity=3)[0]
            logging.info(f"[Backend] Query Reservoir SUCESS: {reservoir_query}")
            all_data.get(factory)[f"reservoir_percentage_{i}"] = reservoir_query["percentage"]
            all_data.get(factory)[f"reservoir_time_{i}"] = reservoir_query["time"].strftime("%Y/%m/%d %p %I:%M")
    except:
        logging.warning(f"[Backend] Query Reservoir FAIL: {factory} !")
    
@app.route('/hsinchu', methods=['GET'])
def hsinchu():
    update_factory_data(factory="hsinchu", all_data=all_data), 200
    return jsonify({'data': all_data.get("hsinchu")})


@app.route('/taichung', methods=['GET'])
def taichung():
    update_factory_data(factory="taichung", all_data=all_data), 200
    return jsonify({'data': all_data.get("taichung")})


@app.route('/tainan', methods=['GET'])
def tainan():
    update_factory_data(factory="tainan", all_data=all_data), 200
    return jsonify({'data': all_data.get("tainan")})


#-------------------------       database       -------------------------#

db = MongoDB()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)