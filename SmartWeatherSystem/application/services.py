from datetime import datetime
from domain.entities import WeatherLog

class WeatherService:
    def __init__(self, api_client, db):
        self.api_client = api_client
        self.db = db

    def get_weather(self, city: str) -> dict:
        data = self.api_client.get_weather(city)

        temp = data.get("main", {}).get("temp")
        weather_list = data.get("weather", [])
        condition = weather_list[0].get("description") if weather_list else "N/A"

        log = WeatherLog(
            city=city,
            temperature=temp,
            condition=condition,
            logged_at=datetime.utcnow()
        )

        self.db.add(log)
        self.db.commit()

        return data
