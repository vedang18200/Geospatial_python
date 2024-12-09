# utils.py (you can add this to your existing app)

import requests

def get_climate_data(city_name):
    # OpenWeatherMap API URL
    api_key = "459f17f5afccee3aefaa1707cb5ee6d0"  # Replace with your actual API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    response = requests.get(base_url)
    data = response.json()

    if response.status_code == 200:
        # Extract relevant data from the response
        climate_info = {
            'city': city_name,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'latitude': data['coord']['lat'],
            'longitude': data['coord']['lon']
        }
        return climate_info
    else:
        return None
