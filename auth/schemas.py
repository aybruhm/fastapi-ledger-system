# Pydantic Imports
from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        schema_extra = {
            "example": "abram@pandaware.tech",
            "password": "fastapi_is_awesome!"
        }