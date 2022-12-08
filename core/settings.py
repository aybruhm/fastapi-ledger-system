# Pydantic Imports
from pydantic import BaseSettings

# Third Party Imports
from decouple import config


class Settings(BaseSettings):
    JWT_SECRET_KEY: str = config("JWT_SECRET")
    JWT_ALGORITHM: str = config("JWT_ALGORITHM")
    TOKEN_LIFETIME: int = 30


ledger_settings = Settings()
