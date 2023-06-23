import requests
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, timedelta
from website.error_enums import ErrorEnum

load_dotenv()
WEATHER_API_KEY = getenv("weather_api")


def get_hourly_weather_data_single_day(location: str, date: str):
    current_time = datetime.now()
    current_hour = current_time.hour

    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&dt={date}&hour=0-23&days=1"

    response = requests.get(url)
    data = response.json()
    try:
        hourly_forecast = data["forecast"]["forecastday"][0]["hour"]
    except IndexError:
        return ErrorEnum.DATE_TOO_FAR_IN_FUTURE

    if date == str(datetime.now().date()):
        hourly_forecast = [
            hour
            for hour in hourly_forecast
            if int(hour["time"].split()[-1].split(":")[0]) > current_hour
        ]

    return hourly_forecast


if __name__ == "__main__":
    pass
