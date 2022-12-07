# Pydantic Imports
from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    email: str
    password: str
