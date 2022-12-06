# Pydantic Imports
from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "your.name@email.com",
                "password": "fastapi_is_awesome!",
            }
        }
