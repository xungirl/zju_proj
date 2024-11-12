'''
Author: Maggie xungirl1024@gmail.com
Date: 2024-11-12 12:45:40
LastEditors: Maggie xungirl1024@gmail.com
LastEditTime: 2024-11-12 13:54:59
FilePath: /zju_proj/app.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class WeatherRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float)
    description = db.Column(db.String(100))
    humidity = db.Column(db.Integer)
    wind_speed = db.Column(db.Float)

with app.app_context():
    db.create_all()

API_KEY = "13014273332be0f221173b22cb4db50d"  # 替换成你的API密钥
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "请提供城市名称"}), 400

    response = requests.get(BASE_URL, params={
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'zh'
    })
    data = response.json()

    if data['cod'] != 200:
        return jsonify({"error": "无法获取天气数据"}), 404

    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }

    new_record = WeatherRecord(
        city=weather_info["city"],
        date=datetime.now().date(),
        temperature=weather_info["temperature"],
        description=weather_info["description"],
        humidity=weather_info["humidity"],
        wind_speed=weather_info["wind_speed"]
    )
    db.session.add(new_record)
    db.session.commit()

    return jsonify(weather_info), 200

@app.route('/api/weather_history', methods=['GET'])
def get_weather_history():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "请提供城市名称"}), 400

    records = WeatherRecord.query.filter_by(city=city).order_by(WeatherRecord.date).all()
    results = [
        {
            "date": record.date.strftime("%Y-%m-%d"),
            "temperature": record.temperature
        } for record in records
    ]
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)