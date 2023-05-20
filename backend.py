from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# 配置 MongoDB 連接
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
mongo = PyMongo(app)

# 向 DB 拿地震資料
@app.route('/earthquake', methods=['GET'])
def get_earthquake_data():
    earthquake_data = mongo.db.earthquake.find()
    result = []
    for data in earthquake_data:
        result.append({
            '地震時間': data['地震時間'],
            '規模(M_L)': data['規模(M_L)'],
            '地震深度(focal dep)': data['地震深度(focal dep)'],
            '經度(東)(longitude)': data['經度(東)(longitude)'],
            '緯度(北)(latitude)': data['緯度(北)(latitude)']
        })
    return jsonify(result)

# 向 DB 拿水庫資料
@app.route('/reservoir', methods=['GET'])
def get_reservoir_data():
    reservoir_data = mongo.db.reservoir.find()
    result = []
    for data in reservoir_data:
        result.append({
            '水情時間': data['水情時間'],
            '有效蓄水量': data['有效蓄水量'],
            '蓄水百分比': data['蓄水百分比']
        })
    return jsonify(result)

# 向 DB 拿供電資料
@app.route('/power', methods=['GET'])
def get_power_data():
    power_data = mongo.db.power.find()
    result = []
    for data in power_data:
        result.append({
            '即時發電量': data['即時發電量'],
            '即時用電量': data['即時用電量'],
            '供電百分比': data['供電百分比']
        })
    return jsonify(result)


if __name__ == '__main__':
    app.run()