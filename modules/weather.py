import os
import requests

def get_weather():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = os.getenv("WEATHER_CITY", "").strip()
    
    if not city or city == "${{ vars.WEATHER_CITY }}" or "vars." in city:
        city = "Bregenz, AT"
        
    city = city.strip("'\"")
    
    if not api_key:
        print("Weather Error: OPENWEATHER_API_KEY is missing!")
        return "Weather N/A"
        
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if response.status_code != 200:
            print(f"Weather API Error: {data.get('message', 'Unknown Error')}")
            return "Weather N/A"
            
        return f"{round(data['main']['temp'])}°C, {data['weather'][0]['description'].title()}"
    except Exception as e:
        print(f"Weather Network Error: {e}")
        return "Weather N/A"