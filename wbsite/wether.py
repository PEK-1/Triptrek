import requests

# OpenWeatherMap API key
API_KEY = "enter your OpenWeatherMAo API here"


def get_lat_lon(city):
    """Get latitude and longitude of a city using OpenWeatherMap's Geocoding API."""
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(url).json()
    if response:
        return response[0]['lat'], response[0]['lon']
    else:
        raise ValueError("Invalid city name or not found.")

def get_current_weather(lat, lon):
    """Fetch the current weather for the given latitude and longitude."""
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    
    # Check if the response is valid
    if response.get('cod') != 200:
        raise ValueError("Error retrieving weather data.")

    weather_description = response['weather'][0]['description']
    temperature = response['main']['temp']
    
    return weather_description, temperature

def www(city):
    if ',' in city:
        try:
            lat, lon = map(float, city.split(','))
        except ValueError:
            raise ValueError("Invalid latitude or longitude format.")
    else:
        lat, lon = get_lat_lon(city)
    weather_description, temperature = get_current_weather(lat, lon)
    print(f"Current weather in {city}: {weather_description}, Temperature: {temperature}°C")
    return temperature
