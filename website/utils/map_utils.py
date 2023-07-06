from website.error_enums import ErrorEnum
import requests
from website.env_loader import GOOGLE_API_KEY
from typing import List, Union


def extract_lat_long_via_address(
    address_or_zipcode: str,
) -> Union[List[float], ErrorEnum]:
    """
    Extracts latitude and longitude coordinates for a given address or zipcode.

    Args:
        address_or_zipcode (str): The address or zipcode for which to retrieve latitude and longitude.

    Returns:
        Union[List[float, float], ErrorEnum]:
            - If successful, returns a list containing the latitude and longitude coordinates as floats.
            - If an error occurs during the API request or processing, returns an ErrorEnum.

    This function makes use of the Google Geocoding API to extract the latitude and longitude coordinates
    for a given address or zipcode. It sends a request to the API with the provided address/zipcode,
    and retrieves the response containing the geocoding information.

    If the request is successful and the API returns valid results, the latitude and longitude coordinates
    are extracted from the response and returned as a list [latitude, longitude]. If not it will return a
    ErrorEnum to indicate the specific error.

    """

    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address_or_zipcode, "key": GOOGLE_API_KEY}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
    except (requests.RequestException, ValueError):
        return ErrorEnum.REQUEST_FAILED

    try:
        """
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        """
        results = response.json()["results"]
        location = results[0]["geometry"]["location"]
        lat = location["lat"]
        lng = location["lng"]
    except Exception:
        return ErrorEnum.INVALID_CITY

    return [lat, lng]


if __name__ == "__main__":
    pass
