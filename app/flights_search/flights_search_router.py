from fastapi import APIRouter
from pydantic import BaseModel

from app.flights_search.flights_search import get_flight_offers, extract_flight_products

flights_search_router = APIRouter()


class RequestSearchKeywords(BaseModel):
    originLocationCode: str
    destinationLocationCode: str
    departureDate: str
    returnDate: str
    nonStop: str
    adults: int
    children: int
    infants: int


@flights_search_router.post('/flights/flight-list')
async def search_flights(request: RequestSearchKeywords):
    data = get_flight_offers(request)
    flights_list = extract_flight_products(data)
    print(flights_list)

    return flights_list
