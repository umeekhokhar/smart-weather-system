from abc import ABC, abstractmethod

class IWeatherService(ABC):
    @abstractmethod
    async def get_weather(self, city: str) -> dict:
        pass