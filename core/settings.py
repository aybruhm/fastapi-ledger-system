# Pydantic Imports
from pydantic import BaseSettings

# Third Party Imports
from decouple import config


class Settings(BaseSettings):
    """Base configuration settings"""

    JWT_SECRET_KEY: str = config("JWT_SECRET")
    JWT_ALGORITHM: str = config("JWT_ALGORITHM")
    TOKEN_LIFETIME: int = 30
    
    TITLE = "Ledger System"
    DESCRIPTION = "A fintech backend ledger system built with FastAPI."
    CONTACT = "israelvictory87@gmail.com"
    LICENSE = "CC0 1.0 Universal"


ledger_settings = Settings()
