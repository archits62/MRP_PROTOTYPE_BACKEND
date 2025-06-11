import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    JWT_SECRET_KEY : str = os.getenv("JWT_SECRET_KEY")
    DB_URL : str = os.getenv("DB_URL")
    ALGORITHM : str = os.getenv("ALGORITHM")