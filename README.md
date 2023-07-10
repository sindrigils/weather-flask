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
   <br />
   `google_maps_api=YOUR_GOOGLE_MAPS_API_KEY`
   <br />
   `secret_key=YOUR_SECRET_KEY`
   <br />
   `mail_username=YOUR_EMAIL_USERNAME`
   <br />
   `mail_password=YOUR_EMAIL_PASSWORD`

   Explanation of the variables:
   <br />
   `weather_api`: Your Weather API key. Obtain this key by signing up here www.weatherapi.com, the free trial is enough.
   <br />
   `google_maps_api`: Your Google Maps API key. Obtain this key by creating a project in the Google Cloud Console and enabling the necessary APIs. Follow these steps to obtain the API key:
      <br />
          1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
      <br />
          2. Create a new project or select an existing project.
      <br />
          3. Enable the "Maps JavaScript API", "Maps Static API" and "Geocode" for your project.
      <br />
          4. Generate an API key for your project.
      <br />
          5. Copy the API key and use it as the value for the `google_maps_api` variable in the `.env` file.
      <br />
   `secret_key`: A secret key used for Flask's session management and other security-related features. Generate a secure random key to use as the value for this variable.
   <br />
   `mail_username`:The email username or address used for sending emails. Provide the email account credentials to be used by the application for sending emails (e.g., password reset, contact form). Please ensure that the provided email account allows sending emails programmatically via SMTP.
   <br />
   `mail_password`: The password for the email account used for sending emails. Provide the corresponding password for the email account.


# Usage

Run the main.py file
or `flask run`
