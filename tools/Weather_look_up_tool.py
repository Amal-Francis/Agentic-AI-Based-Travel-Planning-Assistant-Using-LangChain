import requests
from langchain.tools import tool


@tool
def weather_lookup_tool(location: str):
    """Fetch the current weather for a given city using Open-Meteo"""
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
    geo_data = requests.get(geo_url).json()
    if not geo_data.get('results'):
        return "City not found"

    lat = geo_data['results'][0]['latitude']
    lon = geo_data['results'][0]['longitude']
    weather_url = (

        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
    )
    weather_data = requests.get(weather_url).json()
    temp = weather_data['current_weather']['temperature']
    return temp



