import pickle


FLIGHT_API_DATA_SAVED_FILE = 'app/flight_api/flight_api'

flight_api_info = dict({
    'flight_api_key': 'YOUR_API_KEY',
    'flight_api_secret': 'YOUR_API_SECRET',
})

f = open(FLIGHT_API_DATA_SAVED_FILE, 'wb')
pickle.dump(flight_api_info, f)
f.close()