from dotenv import load_dotenv
from os import getenv

load_dotenv()
GOOGLE_API_KEY = getenv("google_maps_api")
WEATHER_API_KEY = getenv("weather_api")
secret_key = getenv("secret_key")
