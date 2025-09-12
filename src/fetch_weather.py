import requests

def get_weather(city, api_key):
    """
    Fetch weather data for a specific city.

    Args:
        city (str): The city name (e.g., "Hong Kong,HK").
        api_key (str): Your OpenWeatherMap API key.

    Returns:
        dict: Parsed JSON response containing weather data.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch weather data (Status Code: {response.status_code})")
        return None

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    API_KEY = "YOUR_API_KEY"
    CITY = "Hong Kong,HK"

    weather_data = get_weather(CITY, API_KEY)
    if weather_data:
        print("Weather Data for Hong Kong:")
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Wind Speed: {weather_data['wind']['speed']} m/s")
        print(f"Description: {weather_data['weather'][0]['description']}")
