# Pydantic Imports
from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "abram@pandaware.tech",
                "password": "fastapi_is_awesome!",
            }
        }
