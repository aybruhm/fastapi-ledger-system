# Pydantic Imports
from pydantic import BaseSettings

# Third Party Imports
from decouple import config


class Settings(BaseSettings):
    """Base configuration settings"""

    JWT_SECRET_KEY: str = config("JWT_SECRET", cast=str)
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", cast=str)
    TOKEN_LIFETIME: int = config("TOKEN_LIFETIME", cast=int)

    TITLE: str = "Ledger System"
    DESCRIPTION: str = "A fintech backend ledger system built with FastAPI."
    CONTACT: dict = {
        "name": "Abraham Israel",
        "url": "http://linkedin.com/in/abraham-israel",
        "email": "israelvictory87@gmail.com",
    }
    API_VERSION: float = 1.0
    LICENSE: dict = {
        "name": "CC0 1.0 Universal",
        "url": "https://github.com/aybruhm/fastapi-ledger-system/blob/main/LICENSE",
    }


ledger_settings = Settings()
