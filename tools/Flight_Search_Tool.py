from langchain_core.tools import tool
from datetime import datetime
from amadeus import Client, ResponseError, Location
import os
from dotenv import load_dotenv
load_dotenv()


@tool
def search_flights(source: str, destination: str, travel_date: str):
    """Search flight between source and destination cities.
    Args:
        source: Name of the origin city (e.g., 'Hyderabad')
        destination: Name of the destination city (eg., 'Delhi')
        travel_date: Date of travel in 'DD-MM-YY' format
        """
    amadeus = Client(
        client_id=os.getenv("AMADEUS_CLIENT_ID"),
        client_secret=os.getenv('AMADEUS_CLIENT_SECRET')
    )

    def find_loc(city_name: str):
        try:
            location = amadeus.reference_data.locations.get(
                keyword=city_name,
                subType=Location.AIRPORT
            )
            if not location.data:
                return None
            location_code = location.data[0]['iataCode']
            return location_code

        except:
            return None

    source_code = find_loc(source)
    destination_code = find_loc(destination)

    if not source_code or not destination_code:
        return f"Error: could not find airport codes for {source} or {destination}"

    try:
        formatted_date = datetime.strptime(travel_date, '%d-%m-%Y').strftime('%Y-%m-%d')

        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=source_code,
            destinationLocationCode=destination_code,
            departureDate=formatted_date,
            adults=1,


        )

        flights = []
        for offer in response.data:
            price = offer['price']['total']
            final_price = round(float(price) * 105.87, 2)
            currency = 'INR'
            itinerary = offer['itineraries'][0]['segments'][0]
            carrier = itinerary['carrierCode']

            flights.append({
                "airline": carrier,
                'price': f"{currency} {final_price} {'₹'}",
                'departure': itinerary['departure']['at']
                 })
            return flights if flights else "No flights found for this date."
    except ResponseError as error:
        return f"Amadeus API Error: {error}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


