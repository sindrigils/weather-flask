import requests
from datetime import datetime, timedelta
from website.error_enums import ErrorEnum
from website.env_loader import WEATHER_API_KEY
from typing import List, Union, Dict


def get_hourly_weather_data_single_day(
    location: str, selected_date: str
) -> Union[List[Dict[str, str]], ErrorEnum]:
    """
    Retrieves the hourly weather forecast for a specific location and date.

    Args:
        location (str): The location for which to retrieve the weather forecast.
        selected_date (str): The date for which to retrieve the weather forecast in the format "YYYY-MM-DD".

    Returns:
        Union[List[Dict[str, str]], ErrorEnum]:
            - If successful, returns a list of dictionaries representing the hourly weather forecast.
              Each dictionary contains weather data for a specific hour, with keys such as "time", "temperature", etc.
            - If an error occurs during the API request or processing, returns an ErrorEnum.

    This function fetches the hourly weather forecast data from an external API for the specified location and date.
    It constructs the API URL using the provided location and selected date.
    The URL is then used to send a request to the API and retrieve the response.

    If the API request is successful and the response contains valid weather forecast data,
    the function extracts the hourly forecast from the response and returns it as a list of dictionaries.
    Each dictionary represents the weather data for a specific hour, with keys corresponding to different weather attributes.
    If not a ErrorEnum is returned to indicate the specific error.
    """

    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&dt={selected_date}&hour=0-23&days=1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return ErrorEnum.REQUEST_FAILED

    current_time = datetime.now()
    current_hour = current_time.hour

    current_date = current_time.date()
    selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
    diff_between_dates = current_date - selected_date_obj

    if diff_between_dates > timedelta(
        days=2
    ):  # the free trial api plan can only go two days into the past
        return ErrorEnum.DATE_TOO_FAR_IN_PAST

    try:
        hourly_forecast = data["forecast"]["forecastday"][0]["hour"]
    except IndexError:
        return ErrorEnum.DATE_TOO_FAR_IN_FUTURE

    if selected_date == str(datetime.now().date()):
        hourly_forecast = [
            hour
            for hour in hourly_forecast
            if int(hour["time"].split()[-1].split(":")[0]) > current_hour
        ]

    return hourly_forecast


if __name__ == "__main__":
    pass
