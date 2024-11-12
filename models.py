
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建 SQLAlchemy 实例
db = SQLAlchemy()

# 定义数据库模型
class WeatherRecord(db.Model):
    __tablename__ = 'weather_records'  # 设置表名
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float)
    description = db.Column(db.String(100))
    humidity = db.Column(db.Integer)
    wind_speed = db.Column(db.Float)