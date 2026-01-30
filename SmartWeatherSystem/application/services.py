from datetime import datetime
from domain.entities import WeatherLog
from application.weather_interfaces import IWeatherProvider, IObserver, ISubject
from application.factories import AlertFactory

# --- BEHAVIORAL PATTERN: CONCRETE OBSERVER ---
class AlertSystem(IObserver):
    def __init__(self):
        self.latest_alert = None

    def update(self, weather_data: dict):
        # Extract necessary data for decision making
        temp = weather_data.get("main", {}).get("temp", 0)
        weather_list = weather_data.get("weather", [])
        condition = weather_list[0].get("description", "") if weather_list else ""

        # Use Factory to create the specific alert object
        alert_obj = AlertFactory.create_alert(condition, temp)
        
        self.latest_alert = alert_obj.message()
        print(f"[AlertSystem] Generated: {self.latest_alert}")

# --- BEHAVIORAL PATTERN: SUBJECT (SERVICE) ---
class WeatherService(ISubject):
    def __init__(self, provider: IWeatherProvider, db):
        self.provider = provider
        self.db = db
        self._observers = []

    def attach(self, observer: IObserver):
        self._observers.append(observer)

    def notify(self, data: dict):
        for observer in self._observers:
            observer.update(data)

    def get_weather_process(self, city: str, user_id: int):
        # 1. Fetch Current Data (via Adapter)
        current_data = self.provider.fetch_current(city)
        
        # 2. Fetch Forecast Data (via Adapter)
        forecast_data = self.provider.fetch_forecast(city)

        # 3. Log to Database (Individual History)
        temp = current_data.get("main", {}).get("temp")
        cond = current_data.get("weather", [])[0].get("description") if current_data.get("weather") else "N/A"
        
        log = WeatherLog(
            city=city,
            temperature=temp,
            condition=cond,
            logged_at=datetime.utcnow(),
            user_id=user_id  # Feature: Link to User
        )
        self.db.add(log)
        self.db.commit()

        # 4. Notify Observers (Trigger Alerts)
        self.notify(current_data)

        return {
            "current": current_data,
            "forecast": forecast_data
        }