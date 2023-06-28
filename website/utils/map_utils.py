from website.error_enums import ErrorEnum
import requests
from website.env_loader import GOOGLE_API_KEY


def extract_lat_long_via_address(address_or_zipcode):
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
