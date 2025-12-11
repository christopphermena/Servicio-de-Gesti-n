# api/weather_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_by_city(city: str, country_code: str = "CL", units: str = "metric"):
    """
    Retorna diccionario con info básica del clima para la ciudad.
    Requiere OPENWEATHER_API_KEY en .env para hacer la petición real.
    Si falta clave o falla, retorna datos simulados.
    """
    if not city:
        raise ValueError("city requerido")

    if OPENWEATHER_KEY:
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": f"{city},{country_code}", "appid": OPENWEATHER_KEY, "units": units, "lang": "es"}
            resp = requests.get(url, params=params, timeout=6)
            resp.raise_for_status()
            data = resp.json()
            return {
                "city": data.get("name"),
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "raw": data
            }
        except Exception as e:
            # Fall back to dummy
            return {
                "city": city,
                "temp": None,
                "description": f"No se pudo obtener (error: {e})",
                "humidity": None,
                "raw": None
            }
    else:
        # Dummy response if no API key
        return {
            "city": city,
            "temp": 18.5,
            "description": "Parcialmente nublado (simulado)",
            "humidity": 70,
            "raw": None
        }
