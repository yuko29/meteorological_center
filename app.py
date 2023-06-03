from flask import Flask, render_template, jsonify, request, send_from_directory
from mongoDB import mongoDB


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
    "Electricity_value": 2000, "Electricity_maximum": 3000,
    "Earthquake_time": "2022/5/23 下午 6:23:00", "Earthquake_magnitude": "1",
    "Reservoir_name_1": "石門水庫", "Reservoir_percentage_1": f"{40}%",
    "Reservoir_name_2": "寶山第二水庫", "Reservoir_percentage_2": f"{60}%",
    "Reservoir_name_3": "永和山水庫", "Reservoir_percentage_3": f"{80}%"
}

# 中(鯉魚潭水庫、德基水庫)
taichung_data = {
    "Electricity_value": 1000, "Electricity_maximum": 2000,
    "Earthquake_time": "2022/5/24 下午 6:24:00", "Earthquake_magnitude": "2",
    "Reservoir_name_1": "鯉魚潭水庫", "Reservoir_percentage_1": f"{10}%",
    "Reservoir_name_2": "德基水庫", "Reservoir_percentage_2": f"{20}%",
    "Reservoir_name_3": "", "Reservoir_percentage_3": ""
}

# 南(南化水庫、曾文水庫、烏山頭水庫)
tainan_data = {
    "Electricity_value": 500, "Electricity_maximum": 1000,
    "Earthquake_time": "2022/5/25 下午 6:25:00", "Earthquake_magnitude": "3",
    "Reservoir_name_1": "南化水庫", "Reservoir_percentage_1": f"{1}%",
    "Reservoir_name_2": "曾文水庫", "Reservoir_percentage_2": f"{2}%",
    "Reservoir_name_3": "烏山頭水庫", "Reservoir_percentage_3": f"{3}%"
}

@app.route('/hsinchu', methods=['GET'])
def hsinchu():
    
    print("click hsinchu !")
    
    # earthquuake
    earthquake_data = db.retrieveFactoryEarthquake(1, "竹")[0]
    hsinchu_data["Earthquake_time"] = earthquake_data["time"]
    hsinchu_data["Earthquake_magnitude"] = earthquake_data["magnitude"]
    
    # electricity
    electricity_data = db.retrieveElectricity(1, '竹')[0]
    hsinchu_data["Electricity_value"] = electricity_data["power_usage"]
    hsinchu_data["Electricity_maximum"] = electricity_data["power_generate"]
    
    # reservoir
    reservoir_data = db.retrieveReservoir(1, "石門水庫")[0]
    hsinchu_data["Reservoir_percentage_1"] = reservoir_data["percentage"]
    reservoir_data = db.retrieveReservoir(1, "寶山第二水庫")[0]
    hsinchu_data["Reservoir_percentage_2"] = reservoir_data["percentage"]
    reservoir_data = db.retrieveReservoir(1, "永和山水庫")[0]
    hsinchu_data["Reservoir_percentage_3"] = reservoir_data["percentage"]
    
    return jsonify({'data': hsinchu_data})

@app.route('/taichung', methods=['GET'])
def taichung():

    print("click taichung !")
    
    # earthquuake
    earthquake_data = db.retrieveFactoryEarthquake(1, "中")[0]
    taichung_data["Earthquake_time"] = earthquake_data["time"]
    taichung_data["Earthquake_magnitude"] = earthquake_data["magnitude"]
    
    # electricity
    electricity_data = db.retrieveElectricity(1, '中')[0]
    taichung_data["Electricity_value"] = electricity_data["power_usage"]
    taichung_data["Electricity_maximum"] = electricity_data["power_generate"]
    
    # reservoir
    reservoir_data = db.retrieveReservoir(1, "鯉魚潭水庫")[0]
    taichung_data["Reservoir_percentage_1"] = reservoir_data["percentage"]
    reservoir_data = db.retrieveReservoir(1, "德基水庫")[0]
    taichung_data["Reservoir_percentage_2"] = reservoir_data["percentage"]

    return jsonify({'data': taichung_data})

@app.route('/tainan', methods=['GET'])
def tainan():

    print("click tainan !")

    # earthquuake
    earthquake_data = db.retrieveFactoryEarthquake(1, "南")[0]
    tainan_data["Earthquake_time"] = earthquake_data["time"]
    tainan_data["Earthquake_magnitude"] = earthquake_data["magnitude"]
    db.retrieveFactoryEarthquake
    
    # electricity
    electricity_data = db.retrieveElectricity(1, "南")[0]
    tainan_data["Electricity_value"] = electricity_data["power_usage"]
    tainan_data["Electricity_maximum"] = electricity_data["power_generate"]
    
    # reservoir
    reservoir_data = db.retrieveReservoir(1, "南化水庫")[0]
    tainan_data["Reservoir_percentage_1"] = reservoir_data["percentage"]
    reservoir_data = db.retrieveReservoir(1, "曾文水庫")[0]
    tainan_data["Reservoir_percentage_2"] = reservoir_data["percentage"]
    reservoir_data = db.retrieveReservoir(1, "烏山頭水庫")[0]
    tainan_data["Reservoir_percentage_3"] = reservoir_data["percentage"]

    return jsonify({'data': tainan_data})


#-------------------------       database       -------------------------#

db = mongoDB()

earthEqake_test = {'time': '2023-5-12 03:40:52', 'M_L': 3.6, 'focal_dep': 3.2, 'longitude': 41.0, 'latitude': 20.7, 'magnitude': [{'factory': '竹', 'magnitude': 0.00032644588703523386}, {'factory': '中', 'magnitude': 0.00019905740360289052}, {'factory': '南', 'magnitude': 0.0003714193582435097}]}
earthEqake_test2 = {'time': '2023-5-12 03:40:52', 'M_L': 3.6, 'focal_dep': 3.2, 'longitude': 41.0, 'latitude': 20.7, 'magnitude': [{'factory': '竹', 'magnitude': 0.00032644588703523386}, {'factory': '中', 'magnitude': 0.00019905740360289052}, {'factory': '南', 'magnitude': 0.0003714193582435097}]}
electricity_test = {'region':"竹", 'power_usage':512.3, 'power_generate': 482.1, 'time': "2023-5-12 03:40:52"}
electricity_test1 = {'region':"中", 'power_usage':512.3, 'power_generate': 482.1, 'time': "2023-5-12 03:40:52"}
electricity_test2 = {'region':"南", 'power_usage':510.3, 'power_generate': 472.1, 'time': "2023-5-12 03:40:52"}
reservoir_test1 = {'time':"2023-5-12 03:40:52", 'percentage': 427.6, 'water_supply': 321.2, 'name': "鯉魚潭水庫"}
reservoir_test2 = {'time':"2023-5-12 03:40:52", 'percentage': 42.6, 'water_supply': 321.2, 'name': "德基水庫"}
reservoir_test3 = {'time':"2023-5-12 03:40:52", 'percentage': 42.6, 'water_supply': 321.2, 'name': "石門水庫"}
reservoir_test4 = {'time':"2023-5-12 03:40:52", 'percentage': 42.6, 'water_supply': 321.2, 'name': "寶山第二水庫"}
reservoir_test5 = {'time':"2023-5-12 03:40:52", 'percentage': 42.6, 'water_supply': 321.2, 'name': "永和山水庫"}
reservoir_test6 = {'time':"2023-5-12 03:40:52", 'percentage': 42.6, 'water_supply': 321.2, 'name': "南化水庫"}
reservoir_test7 = {'time':"2023-5-12 03:40:52", 'percentage': 42.6, 'water_supply': 321.2, 'name': "曾文水庫"}
reservoir_test8 = {'time':"2023-5-12 03:40:52", 'percentage': 42.6, 'water_supply': 321.2, 'name': "烏山頭水庫"}

db.insertEarthquake(earthEqake_test)
db.insertEarthquake(earthEqake_test2)
db.insertElectricity(electricity_test)
db.insertElectricity(electricity_test1)
db.insertElectricity(electricity_test2)
db.insertReservoir(reservoir_test1)
db.insertReservoir(reservoir_test2)
db.insertReservoir(reservoir_test3)
db.insertReservoir(reservoir_test4)
db.insertReservoir(reservoir_test5)
db.insertReservoir(reservoir_test6)
db.insertReservoir(reservoir_test7)
db.insertReservoir(reservoir_test8)


if __name__ == '__main__':
    app.run(port=5022)
