from langchain.tools import tool
from tools.json_download import load_json

@tool
def recommend_hotel(city: str, max_price: int =5000):
    """Recommend best hotel based on rating and price"""
    hotels = load_json('tools/hotels.json')
    filtered = [
        h for h in hotels
        if h['city'].lower() == city.lower()
        and h['price_per_night'] <= max_price
    ]
    if not filtered:
        return "No hotels found"
    return filtered

