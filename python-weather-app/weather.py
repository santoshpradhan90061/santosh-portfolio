
from datetime import datetime
import requests

weather_conditions = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail"
}

weather_icons = {
    0: "☀️",
    1: "🌤️",
    2: "⛅",
    3: "☁️",
    45: "🌫️",
    48: "🌫️",
    51: "🌦️",
    53: "🌦️",
    55: "🌧️",
    61: "🌧️",
    63: "🌧️",
    65: "⛈️",
    71: "🌨️",
    73: "❄️",
    75: "❄️",
    95: "⛈️",
    96: "⛈️",
    99: "⛈️"
}


def get_weather(city):

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        geo_url, params=geo_params, timeout=15
    )
    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        print("City not found!")
        return None

    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]
    city_name = data["results"][0]["name"]

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "forecast_days": 5,
        "timezone": "auto"
    }

    weather_response = requests.get(
        weather_url, params=weather_params, timeout=15
    )
    weather_response.raise_for_status()

    return city_name, weather_response.json()


def show_current_weather(city_name, weather_data):

    current = weather_data["current"]
    code = current["weather_code"]

    icon = weather_icons.get(code, "🌡️")
    condition = weather_conditions.get(code, "Unknown condition")

    print("\n===== CURRENT WEATHER =====")
    print("City:", city_name)
    print("Temperature:", current["temperature_2m"], "°C")
    print("Feels Like:", current["apparent_temperature"], "°C")
    print("Humidity:", current["relative_humidity_2m"], "%")
    print("Wind Speed:", current["wind_speed_10m"], "km/h")
    print("Weather:", icon, condition)


def show_forecast(city_name, weather_data):

    daily = weather_data["daily"]

    print("\n===== 5-DAY WEATHER FORECAST =====")
    print("City:", city_name)

    for i in range(len(daily["time"])):

        date = daily["time"][i]

        day_name = datetime.strptime(
            date, "%Y-%m-%d"
        ).strftime("%A")

        max_temp = daily["temperature_2m_max"][i]
        min_temp = daily["temperature_2m_min"][i]
        code = daily["weather_code"][i]

        condition = weather_conditions.get(
            code, "Unknown condition"
        )

        icon = weather_icons.get(code, "🌡️")

        print("\n------------------------------")
        print("Day:", day_name)
        print("Date:", date)
        print("Weather:", icon, condition)
        print("Maximum Temperature:", max_temp, "°C")
        print("Minimum Temperature:", min_temp, "°C")


try:

    city = input("Enter city name: ")

    while True:

        print("\n========== WEATHER APP ==========")
        print("1. Check Current Weather")
        print("2. View 5-Day Forecast")
        print("3. Search Another City")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice in ("1", "2"):

            result = get_weather(city)

            if result:
                city_name, weather_data = result

                if choice == "1":
                    show_current_weather(city_name, weather_data)

                else:
                    show_forecast(city_name, weather_data)

        elif choice == "3":

            city = input("Enter another city name: ")

        elif choice == "4":

            print("Thank you for using Weather App!")
            break

        else:
            print("Invalid choice! Please enter 1, 2, 3 or 4.")

except requests.exceptions.RequestException:
    print("Unable to connect to the weather service. Check your internet connection.")
