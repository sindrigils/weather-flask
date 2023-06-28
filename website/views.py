from flask import render_template, Blueprint, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .utils.map_utils import extract_lat_long_via_address
from .utils.weather_utils import get_hourly_weather_data_single_day
from website.error_enums import ErrorEnum
from website.utils.helper import format_date

views = Blueprint("views", __name__)


@views.route("/", methods=["POST", "GET"])
@login_required
def home_page():
    if request.method == "POST":
        city = request.form.get("city")
        date = request.form.get("date")

        if city == "" or date == "":
            flash(message=f"Please enter a city and select a date!", category="danger")
            return redirect(url_for("views.home_page"))

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
    lat_and_lng = extract_lat_long_via_address(city)

    if isinstance(lat_and_lng, ErrorEnum):
        flash(message=f"{lat_and_lng.value}", category="danger")
        return redirect(url_for("views.home_page"))

    data_obj = get_hourly_weather_data_single_day(city, date)

    if isinstance(data_obj, ErrorEnum):
        flash(message=f"{data_obj.value}", category="danger")
        return redirect(url_for("views.home_page"))

    date = format_date(date=date)
    current_user.update_history(city=city, date=date)

    return render_template(
        "weather-page.html",
        city=city.title(),
        date=date[:7],  # I don't want to display the year
        data_obj=data_obj,
        lat=lat_and_lng[0],
        lng=lat_and_lng[1],
    )


@views.route("/profile")
@login_required
def profile_page():
    return render_template(
        "profile-page.html",
        search_history=current_user.search_history[::-1]
        # reverse the search history in order for the newest to be on top
    )
