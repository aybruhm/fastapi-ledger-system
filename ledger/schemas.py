# Pydantic Imports
from pydantic import BaseModel


class WalletBase(BaseModel):
    amount: int


class WalletCreate(WalletBase):
    user: int
    title: str
    
    
class WalletDeposit(WalletBase):
    pass


class WalletWithdraw(WalletBase):
    pass


class Wallet(WalletBase):
    id: int
    user: int
    title: str

    class Config:
        # Without orm_mode, if you returned a SQLAlchemy
        # model from your path operation,
        # it wouldn't include the relationship data
        orm_mode = True


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
