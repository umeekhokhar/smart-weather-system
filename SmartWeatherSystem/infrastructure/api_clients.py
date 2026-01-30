import requests

class OpenWeatherAdapter:
    # OpenWeather Endpoints
    GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
    ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"
    
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _get_coords(self, city: str) -> tuple:
        """Helper to map City Name -> (Lat, Lon)"""
        params = {"q": city, "limit": 1, "appid": self.api_key}
        response = requests.get(self.GEO_URL, params=params)
        
        if response.status_code == 200 and len(response.json()) > 0:
            geo_data = response.json()[0]
            return geo_data['lat'], geo_data['lon'], geo_data.get('country')
        return None, None, None

    def fetch_current(self, city: str) -> dict:
        lat, lon, country = self._get_coords(city)
        if lat is None:
            return {"error": "City not found"}

        try:
            params = {
                "lat": lat, "lon": lon, 
                "appid": self.api_key, "units": "metric",
                "exclude": "minutely,hourly,daily,alerts"
            }
            
            response = requests.get(self.ONECALL_URL, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                current = data["current"]
                # Transform to your interface's expected format
                return {
                    "main": {
                        "temp": current.get("temp"),
                        "humidity": current.get("humidity")
                    },
                    "weather": [{
                        "description": current["weather"][0]["description"],
                        "main": current["weather"][0]["main"]
                    }],
                    "wind": {"speed": current.get("wind_speed")},
                    "sys": {"country": country}
                }
            return {"error": f"API Error: {response.status_code}"}
            
        except Exception as e:
            print(f"Connection Error: {e}")
            return {"main": {"temp": 0}, "weather": [{"description": "error"}]}

    def fetch_forecast(self, city: str) -> dict:
        lat, lon, _ = self._get_coords(city)
        if lat is None: return {"list": []}

        try:
            params = {
                "lat": lat, "lon": lon, 
                "appid": self.api_key, "units": "metric",
                "exclude": "current,minutely,hourly,alerts"
            }
            response = requests.get(self.ONECALL_URL, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                forecast_list = []
                # One Call 3.0 returns 8 days of data in 'daily'
                for day in data.get("daily", []):
                    forecast_list.append({
                        "dt": day.get("dt"),
                        "main": {"temp": day["temp"]["day"]},
                        "weather": day["weather"]
                    })
                return {"list": forecast_list}
            return {"list": []}
        except Exception:
            return {"list": []}