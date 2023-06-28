from flask import Blueprint, request, make_response
import requests
from website.env_loader import GOOGLE_API_KEY

proxy = Blueprint("proxy", __name__)


@proxy.route("/static-image-proxy")
def static_image_proxy():
    city = request.args.get("city")
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {"center": city, "zoom": 15, "size": "600x400", "key": GOOGLE_API_KEY}

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        image_data = response.content
        response = make_response(image_data)
        response.headers.set("Content-Type", "image/png")
        return response

    return "Error occured while fetching static image", 500


@proxy.route("/api/maps")
def maps_proxy():
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
        return "Error occurred while fetching map data", 500
