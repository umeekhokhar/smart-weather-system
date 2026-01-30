from abc import ABC, abstractmethod

# Abstract Product
class WeatherAlert(ABC):
    @abstractmethod
    def message(self) -> str:
        pass

# Concrete Products
class RainAlert(WeatherAlert):
    def message(self) -> str:
        return "🌧️ ALERT: Rain detected! Bring an umbrella."

class SnowAlert(WeatherAlert):
    def message(self) -> str:
        return "❄️ ALERT: Snowfall detected! Drive carefully."

class HeatAlert(WeatherAlert):
    def message(self) -> str:
        return "🔥 ALERT: Extreme heat! Stay hydrated."

class StormAlert(WeatherAlert):
    def message(self) -> str:
        return "⚡ ALERT: Thunderstorm! Stay indoors."

class ClearAlert(WeatherAlert):
    def message(self) -> str:
        return "✅ Conditions are clear."

# --- CREATIONAL PATTERN: FACTORY METHOD ---
class AlertFactory:
    @staticmethod
    def create_alert(condition: str, temp: float) -> WeatherAlert:
        cond_lower = condition.lower()
        
        if "rain" in cond_lower or "drizzle" in cond_lower:
            return RainAlert()
        elif "snow" in cond_lower:
            return SnowAlert()
        elif "thunder" in cond_lower or "storm" in cond_lower:
            return StormAlert()
        elif temp > 35.0:
            return HeatAlert()
        else:
            return ClearAlert()