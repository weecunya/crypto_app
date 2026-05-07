import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY:str = os.getenv('API_KEY')

settings = Settings()