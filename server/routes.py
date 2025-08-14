from flask import Blueprint, jsonify
from server.models.WeatherRecord import WeatherRecord
from collections import defaultdict

weather_routes = Blueprint("weather_bp", __name__)


@weather_routes.route("/weather-chart", methods=["GET"])
def get_weather_data():
    weather_records = WeatherRecord.query.order_by(WeatherRecord.added_at).all()

    weather_data = defaultdict(list)
    for weather_rec in weather_records:
        weather_data[weather_rec.city_name].append({
            "x": weather_rec.added_at.strftime("%Y-%m-%d"),
            "y": weather_rec.temperature
        })

    weather_chart_data = [{"name": city, "data": data} for city, data in weather_data.items()]

    return jsonify(weather_chart_data)