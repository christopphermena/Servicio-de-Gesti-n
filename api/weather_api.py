# api/weather_api.py
"""
Módulo para consultar WeatherAPI y retornar información básica del clima REAL.
"""
import requests

API_KEY = "06d6673168454f36ae3164136251212"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def get_weather_data(city):
    """
    Consulta el clima actual de la localidad indicada usando WeatherAPI.
    Retorna: {'temp': temperatura en °C, 'desc': descripción}
    """
    params = {"key": API_KEY, "q": city, "lang": "es"}
    try:
        resp = requests.get(BASE_URL, params=params, timeout=5)
        data = resp.json()
        if 'current' in data:
            temp = data['current']['temp_c']
            desc = data['current']['condition']['text']
            return {"temp": temp, "desc": desc}
        else:
            raise Exception(data.get('error', {}).get('message', 'No se pudo consultar WeatherAPI.'))
    except Exception as e:
        raise Exception(f"WeatherAPI error: {e}")
