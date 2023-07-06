from flask import Blueprint, request, make_response
import requests
from website.env_loader import GOOGLE_API_KEY
from website.error_enums import ErrorEnum
from typing import Tuple, Union, Dict

proxy = Blueprint("proxy", __name__)


@proxy.route("/static-image-proxy")
def static_image_proxy() -> Union[bytes, Tuple[ErrorEnum, int]]:
    """
    Proxy route for retrieving a static map image for a specific city.

    Retrieves a static map image for the specified city using the Google Maps Static API.
    The city is obtained from the request query parameters.
    The image is requested with a specific center, zoom level, and size.
    If the image retrieval is successful (status code 200), the image data is returned as the response.
    Otherwise, an ErrorEnum.ERROR_FETCHING_IMAGE is returned with a status code of 500.

    Returns:
        Union[bytes, Tuple[ErrorEnum, int]]: The image data as bytes, or an error enum with a status code.
    """

    city = request.args.get("city")
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {"center": city, "zoom": 15, "size": "600x400", "key": GOOGLE_API_KEY}

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        image_data = response.content
        response = make_response(image_data)
        response.headers.set("Content-Type", "image/png")
        return response

    return ErrorEnum.ERROR_FETCHING_IMAGE, 500


@proxy.route("/api/maps")
def maps_proxy() -> Union[Tuple[bytes, int, Dict[str, str]], Tuple[ErrorEnum, int]]:
    """
    Proxy route for retrieving Google Maps API JavaScript for a specific location.

    Retrieves the Google Maps API JavaScript for the specified latitude and longitude.
    The latitude and longitude values are obtained from the request query parameters.
    The JavaScript is requested with the corresponding parameters and the API key.
    If the retrieval is successful (status code 200), the JavaScript content is returned as the response
    with the appropriate content type.
    Otherwise, an ErrorEnum.ERROR_FETCHING_MAP is returned with a status code of 500.

    Returns:
        Tuple[bytes, int, Dict[str, str]]: The JavaScript content as bytes, status code, and response headers.

    """

    try:
        lat = float(request.args.get("lat"))
        lng = float(request.args.get("lng"))
        url = f"https://maps.googleapis.com/maps/api/js?key={GOOGLE_API_KEY}&lat={lat}&lng={lng}&callback=initMap"
        response = requests.get(url)
        return (
            response.content,
            response.status_code,
            {"Content-Type": "application/javascript"},
        )
    except Exception:
        return ErrorEnum.ERROR_FETCHING_MAP, 500
