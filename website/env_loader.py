from dotenv import load_dotenv
from os import getenv

load_dotenv()
GOOGLE_API_KEY = getenv("google_maps_api")
WEATHER_API_KEY = getenv("weather_api")
SECRET_KEY = getenv("secret_key")
MAIL_USERNAME = getenv("mail_username")
MAIL_PASSWORD = getenv("mail_password")
