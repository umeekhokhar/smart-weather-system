from flask import Blueprint, request, jsonify
from infrastructure.data import get_db
from infrastructure.api_clients import WeatherApiClient
from application.services import WeatherService

weather_bp = Blueprint("weather", __name__, url_prefix="/api")

@weather_bp.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "city query parameter is required"}), 400

    db = next(get_db())
    service = WeatherService(WeatherApiClient(), db)

    data = service.get_weather(city)
    return jsonify(data)
