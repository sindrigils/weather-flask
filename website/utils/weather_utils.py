import requests
from datetime import datetime, timedelta
from website.error_enums import ErrorEnum
from website.env_loader import WEATHER_API_KEY


def get_hourly_weather_data_single_day(location: str, selected_date: str):
    """
    Retrieves the hourly weather forecast for a specific location and date.

    Args:
        location (str): The location for which to retrieve the weather forecast.
        selected_date (str): The date for which to retrieve the weather forecast in the format "YYYY-MM-DD".

    Returns:
        list or ErrorEnum: The hourly weather forecast data for the specified date, or an error enum if an error occurs.

    The function fetches the weather forecast data from an external API for the specified location and date.
    It checks if the selected date is within the allowed range (up to two days in the past).
    If the selected date is beyond the allowed range, it returns an error enum indicating the date is too far in the past.
    If the selected date is in the future (beyond the available forecast), it returns an error enum for that scenario as well.
    The function processes the hourly forecast based on the selected date and the current hour, excluding past hours if applicable.
    Finally, it returns the hourly forecast data or an error enum, depending on the result.


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
