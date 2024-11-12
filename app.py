
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime
import requests
from models import db, WeatherRecord  # 导入数据库模型和SQLAlchemy实例

app = Flask(__name__)
CORS(app)

# 配置数据库 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

API_KEY = "13014273332be0f221173b22cb4db50d"  # 替换成你的API密钥
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# 创建数据库表
with app.app_context():
    db.create_all()

# 路由：渲染前端页面
@app.route('/')
def index():
    return render_template('index.html')

# 获取天气的API
@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "请提供城市名称"}), 400

    # 调用外部API获取天气数据
    response = requests.get(BASE_URL, params={
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'zh'
    })
    data = response.json()

    if data['cod'] != 200:
        return jsonify({"error": "无法获取天气数据"}), 404

    # 提取天气信息
    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }

    # 将数据保存到数据库
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

# 获取天气历史记录的API
@app.route('/api/weather_history', methods=['GET'])
def get_weather_history():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "请提供城市名称"}), 400

    records = WeatherRecord.query.filter_by(city=city).order_by(WeatherRecord.date).all()
    results = [
        {
            "date": record.date.strftime("%Y-%m-%d"),
            "temperature": record.temperature,
            "description": record.description,
            "humidity": record.humidity,
            "wind_speed": record.wind_speed
        } for record in records
    ]
    return jsonify(results), 200

# 删除指定城市的所有历史记录的API
@app.route('/api/delete_history', methods=['DELETE'])
def delete_weather_history():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "请提供城市名称"}), 400

    # 删除指定城市的所有记录
    records = WeatherRecord.query.filter_by(city=city).all()
    if records:
        for record in records:
            db.session.delete(record)
        db.session.commit()
        return jsonify({"message": f"{city} 的所有记录已删除"}), 200
    else:
        return jsonify({"error": "未找到该城市的记录"}), 404
    
if __name__ == '__main__':
    app.run(debug=True)