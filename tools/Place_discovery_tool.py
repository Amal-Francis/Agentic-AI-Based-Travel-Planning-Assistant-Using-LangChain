from langchain.tools import tool
from tools.json_download import load_json


@tool
def discover_places(city: str):
    """Find popularr places to visit"""
    places = load_json('tools/places.json')
    return [
               p for p in places
               if p['city'].lower() == city.lower()
                  and p['rating'] >= 4

           ][:5]

