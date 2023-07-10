from flask import render_template, Blueprint, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .utils.map_utils import extract_lat_long_via_address
from .utils.weather_utils import get_hourly_weather_data_single_day
from website.error_enums import ErrorEnum
from datetime import datetime
from website.forms import ContactForm
from website.utils.emails_utils import send_email_to_website


views = Blueprint("views", __name__)


@views.route("/", methods=["POST", "GET"])
@login_required
def home_page():
    """
    Renders the home page and handles the city and date form submission.

    If the request method is "POST":
    - Retrieves the submitted city and date from the request form.
    - If the city or date is empty, flashes an error message and redirects to the home page.
    - Redirects to the weather page for the specified city and date.

    Returns:
        If the request method is "POST", redirects to the weather page.
        If the request method is "GET", renders the "home-page.html" template.
    """

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


@views.route("/contact", methods=["POST", "GET"])
@login_required
def contact_page():
    """
    Renders the contact page and handles the contact form submission.

    If the request method is "GET", initializes a new instance of the ContactForm.

    If the request method is "POST":
    - Validates the submitted contact form.
    - Sends an email to the website with the message from the contact form.
    - Flashes an informational message to confirm the message submission.
    - Redirects to the home page.

    Returns:
        If the request method is "GET", renders the "contact-page.html" template with the contact form.
        If the request method is "POST", redirects to the home page.
    """

    contact_form = ContactForm()

    if contact_form.validate_on_submit():
        send_email_to_website(contact_form.text_area.data)
        flash(
            message=f"We have received your message and we'll respond as fast as possible!",
            category="info",
        )

        return redirect(url_for("views.home_page"))

    return render_template("contact-page.html", form=contact_form)


@views.route("/weather/<city>/<date>")
@login_required
def weather_page(city: str, date: str):
    """
    Renders the weather page for a specific city and date.

    Args:
        city (str): The name of the city.
        date (str): The date in the format "YYYY-MM-DD".

    Returns:
        If successful, renders the "weather-page.html" template with the following parameters:
            - city: Titlecased city name.
            - date: Formatted date (month and year).
            - data_obj: Object containing hourly weather data for the specified city and date.
            - lat: Latitude of the city.
            - lng: Longitude of the city.
        If unsuccessful, flashes an error message and redirects to the home page.
    """

    lat_and_lng = extract_lat_long_via_address(city)

    if isinstance(lat_and_lng, ErrorEnum):
        flash(message=f"{lat_and_lng.value}", category="danger")
        return redirect(url_for("views.home_page"))

    data_obj = get_hourly_weather_data_single_day(city, date)

    if isinstance(data_obj, ErrorEnum):
        flash(message=f"{data_obj.value}", category="danger")
        return redirect(url_for("views.home_page"))

    date_ = datetime.strptime(date, "%Y-%m-%d")
    date = date_.strftime("%d %B %Y")
    current_user.update_history(city=city)

    return render_template(
        "weather-page.html",
        city=city.title(),
        date=date[:7],  # I don't want to display the year
        data_obj=data_obj,
        lat=lat_and_lng[0],
        lng=lat_and_lng[1],
    )


@views.route("/profile", methods=["POST", "GET"])
@login_required
def profile_page():
    """
    Renders the profile page and handles profile picture upload.

    If the request method is "POST", checks if a profile picture is included in the request files.
    If a profile picture is present, updates the current user's profile picture.
    Redirects to the profile page after processing the request.

    If the request method is "GET":
    - Validates the current user's profile picture.
    - Retrieves today's date and formats it.
    - Renders the "profile-page.html" template with the following parameters:
        - search_history: Reversed list of the current user's search history.
        - todays_date: Formatted string of today's date.
        - top_locations: List of the current user's top viewed cities.

    Returns:
        A rendered HTML template of the profile page.
    """

    if request.method == "POST":
        if "profile-pic" in request.files:
            file = request.files["profile-pic"]
            if file.filename != "":
                current_user.update_profile_pic(file)

        return redirect(url_for("views.profile_page"))

    current_user.validate_profile_pic()
    today_date = datetime.utcnow()
    today_date_formatted = datetime.strftime(today_date, "%Y-%m-%d")
    return render_template(
        "profile-page.html",
        search_history=current_user.search_history[::-1],
        # reverse the search history in order for the newest to be on top
        todays_date=today_date_formatted,
        top_locations=current_user.get_top_viewed_cities(),
    )
