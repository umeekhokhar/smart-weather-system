import requests

class WeatherApiClient:
    BASE_URL = "https://open-weather13.p.rapidapi.com/city"

    API_KEY = "7eee175762msh1ef72b95e179907p141e71jsnbaf8735c05f4"
    API_HOST = "open-weather13.p.rapidapi.com"

    def get_weather(self, city: str, lang: str = "EN") -> dict:
        headers = {
            "x-rapidapi-key": self.API_KEY,
            "x-rapidapi-host": self.API_HOST
        }

        querystring = {
            "city": city,
            "lang": lang
        }

        response = requests.get(
            self.BASE_URL,
            headers=headers,
            params=querystring,
            timeout=10
        )

        response.raise_for_status()
        return response.json()
