import requests
import pickle

FLIGHT_API_DATA_SAVED_FILE = 'flight_api/flight_api'

def get_access_token():
    with open(FLIGHT_API_DATA_SAVED_FILE, 'rb') as f:
        flight_api_info = pickle.load(f)

    api_key = flight_api_info['flight_api_key']
    api_secret = flight_api_info['flight_api_secret']

    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return access_token
    else:
        print(f"토큰 요청 실패: {response.status_code}")
        return None



def get_flight_offers():
    access_token = get_access_token()

    if not access_token:
        print("토큰 발급 실패")
        return

    endpoint = "https://test.api.amadeus.com/v2//shopping/flight-offers"

    # 검색 파라미터
    params = {
        "originLocationCode": "ICN",
        "destinationLocationCode": "LAX",
        "departureDate": "2023-08-01",
        "returnDate": "2023-08-16",
        "adults": 1,
        "currencyCode": "KRW",
        "nonStop": "true",
        "max": 5
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(endpoint, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"API 요청 실패: {response.status_code}")


def extract_flight_products(data):
    products = []

    for product in data['data']:
        product_info = {}

        # 왕복 항공권 정보인지 확인
        if len(product['itineraries']) > 1:
            outbound_segments = product['itineraries'][0]['segments']
            inbound_segments = product['itineraries'][1]['segments']

            carrier_code = product['validatingAirlineCodes'][0]
            carrier_name = data['dictionaries']['carriers'][carrier_code]

            outbound_flights = []
            for outbound_segment in outbound_segments:
                flight_info = {}
                flight_info['origin'] = outbound_segment['departure']['iataCode']
                flight_info['destination'] = outbound_segment['arrival']['iataCode']
                flight_info['departure_time'] = outbound_segment['departure']['at']
                flight_info['arrival_time'] = outbound_segment['arrival']['at']
                flight_info['airline'] = carrier_name
                outbound_flights.append(flight_info)

            inbound_flights = []
            for inbound_segment in inbound_segments:
                flight_info = {}
                flight_info['origin'] =inbound_segment['departure']['iataCode']
                flight_info['destination'] = inbound_segment['arrival']['iataCode']
                flight_info['departure_time'] = inbound_segment['departure']['at']
                flight_info['arrival_time'] = inbound_segment['arrival']['at']
                flight_info['airline'] = carrier_name
                inbound_flights.append(flight_info)

            product_info = {
                'outbound flights': outbound_flights,
                'inbound flights': inbound_flights,
                'price': float(product['price']['total']),
                'seats left': product['numberOfBookableSeats'],
            }
            products.append(product_info)


        else:
            outbound_segments = product['itineraries'][0]['segments']
            carrier_code = product['validatingAirlineCodes'][0]
            carrier_name = data['dictionaries']['carriers'][carrier_code]

            outbound_flights = []
            for outbound_segment in outbound_segments:
                flight_info = {}
                flight_info['origin'] = outbound_segment['departure']['iataCode']
                flight_info['destination'] = outbound_segment['arrival']['iataCode']
                flight_info['departure_time'] = outbound_segment['departure']['at']
                flight_info['arrival_time'] = outbound_segment['arrival']['at']
                flight_info['airline'] = carrier_name
                outbound_flights.append(flight_info)

            product_info = {
                'outbound flights': outbound_flights,
                'price': float(product['price']['total']),
                'seats left': product['numberOfBookableSeats'],
            }
            products.append(product_info)