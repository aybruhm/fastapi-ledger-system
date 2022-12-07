# Own Imports
from schemas.ledger import BaseModel, Wallet


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    wallets: list[Wallet] = []

    class Config:
        orm_mode = True
