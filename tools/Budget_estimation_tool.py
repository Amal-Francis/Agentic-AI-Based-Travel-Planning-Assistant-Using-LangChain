from langchain.tools import tool
@tool
def estimate_budget(flight_price: int, hotel_price: int, days: int):
    """Estimate total travel budget"""
    food_transport = days * 1000
    total = flight_price + (hotel_price * days) +  food_transport
    return {
        "Flight" : flight_price,
        'Hotel' : hotel_price * days,
        'Food _transport': food_transport,
        'Total': total
    }