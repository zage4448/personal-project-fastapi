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