import requests
from datetime import datetime

def deg_to_direction(deg):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    ix = round(deg / 45) % 8
    return directions[ix]

def get_weather(city):
    api_key = 'OPEN_WEATHER_API'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fr'

    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return {"error": data.get("message", "Impossible de récupérer les données météo.")}

    # Extraction des données
    temp_min = data["main"]["temp_min"]
    temp_max = data["main"]["temp_max"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    wind_deg = data["wind"].get("deg", 0)
    wind_dir = deg_to_direction(wind_deg)
    description = data["weather"][0]["description"].capitalize()
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S')
    current_time = datetime.fromtimestamp(data["dt"]).strftime('%Y-%m-%d %H:%M:%S')

    # Retourner les résultats sous forme de dictionnaire
    weather_info = {
        "city": city.capitalize(),
        "current_time": current_time,
        "description": description,
        "temp_max": f"{temp_max}°C",
        "temp_min": f"{temp_min}°C",
        "humidity": f"{humidity}%",
        "wind_speed": f"{wind_speed} m/s ({wind_dir})",
        "sunrise": sunrise,
        "sunset": sunset
    }

    return weather_info
