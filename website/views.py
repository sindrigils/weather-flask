from flask import render_template, Blueprint, flash, request, redirect, url_for
from flask_login import login_required
from .utils.map_utils import extract_lat_long_via_address
from .utils.weather_utils import get_hourly_weather_data_single_day
from dotenv import load_dotenv
from website.error_enums import ErrorEnum
import os


load_dotenv()
GOOGLE_API_KEY = os.getenv("google_maps_api")

views = Blueprint("views", __name__)


@views.route("/", methods=["POST", "GET"])
@login_required
def home_page():
    if request.method == "POST":
        city = request.form.get("city")
        date = request.form.get("date")  # 2023-06-13

        # # laga
        # lat, lng = extract_lat_long_via_address(city)
        # if (lat is None) or (lng is None):
        #     flash(
        #         message=f"That's not a valid city {city}! Please try another city",
        #         category="danger",
        #     )
        # return redirect(url_for("views.home_page"))

        return redirect(
            url_for(
                "views.weather_page",
                city=city,
                date=date,
            )
        )

    return render_template("home-page.html")


@views.route("/contact")
@login_required
def contact_page():
    return render_template("contact-page.html")


@views.route("/weather/<city>/<date>")
@login_required
def weather_page(city: str, date: str):
    lat, lng = extract_lat_long_via_address(city)
    data_obj = get_hourly_weather_data_single_day(city, date)

    if data_obj == ErrorEnum.DATE_TOO_FAR_IN_FUTURE:
        flash(message=f"{ErrorEnum.DATE_TOO_FAR_IN_FUTURE.value}", category="danger")
        return redirect(url_for("views.home_page"))

    return render_template(
        "weather-page.html",
        city=city.title(),
        date=date,
        data_obj=data_obj,
        lat=lat,
        lng=lng,
        api_key=GOOGLE_API_KEY,
    )
