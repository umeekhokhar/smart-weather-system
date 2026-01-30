from abc import ABC, abstractmethod

# --- STRUCTURAL PATTERN: ADAPTER INTERFACE ---
class IWeatherProvider(ABC):
    @abstractmethod
    def fetch_current(self, city: str) -> dict:
        pass
    
    @abstractmethod
    def fetch_forecast(self, city: str) -> dict:
        pass

# --- BEHAVIORAL PATTERN: OBSERVER INTERFACE ---
class IObserver(ABC):
    @abstractmethod
    def update(self, weather_data: dict):
        pass

class ISubject(ABC):
    @abstractmethod
    def attach(self, observer: IObserver):
        pass

    @abstractmethod
    def notify(self, data: dict):
        pass