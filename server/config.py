import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENWEATHER_API_KEY=os.getenv("OPEN_WEATHER_API_KEY")