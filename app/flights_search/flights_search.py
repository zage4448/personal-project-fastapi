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