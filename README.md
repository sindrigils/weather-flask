# Weather Flask

This is a Flask web application that provides weather information for different cities. It utilizes weather data from a weather API and integrates with Google Maps for location-based services.

# Installation

1. Clone this repository:
   <br />
   `git clone https://github.com/sindrigils/weather-flask.git`

2. Navigate to the project directory:
   <br />
   `cd weather-flask`

3. Create and activate a virtual environment:
   For Linux/Max:
   <br />
   `python3 -m venv venv`
   <br />
   `source venv/bin/activate`

   For Windows:
   <br />
   `python -m venv venv`
   <br />
   `venv\Scripts\activate`

4. Install the required dependencies:
   <br />
   `pip install -r requirements.txt`

6. Create a .env file in the root directory of the project and provide the following variables:
   <br />
   `weather_api=YOUR_WEATHER_API_KEY`
   `google_maps_api=YOUR_GOOGLE_MAPS_API_KEY`
   `secret_key=YOUR_SECRET_KEY`
   `mail_username=YOUR_EMAIL_USERNAME`
   `mail_password=YOUR_EMAIL_PASSWORD`

# Usage

Run the main.py file
or `flask run`
