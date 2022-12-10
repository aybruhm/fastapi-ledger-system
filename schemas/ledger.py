# Pydantic Imports
from pydantic import BaseModel, validator

# FastAPI & SQLAlchemy Imports
from fastapi import HTTPException
from sqlalchemy.orm import Session

# Core Imports
from config.database import SessionLocal

# Models Imports
from models.ledger import Wallet as UserWallet


class WalletBase(BaseModel):
    user: int
    amount: int


class WalletCreate(WalletBase):
    title: str

    @validator("user", pre=True)
    def ensure_user_can_only_have_one_wallet(cls, value: int):
        """
        Validation to ensure that the user can only have 10 wallets,
        otherwise; raise an error. `@validator("user", pre=True)` means
        that it will be called before the `user` field is validated

        :param cls: The class of the model that is being validated

        :param value: The value of the field being validated
        :type value: int

        :return: The value of the user_wallet_counts
        """
        db: Session = SessionLocal()
        user_wallet_counts = (
            db.query(UserWallet)
            .join(UserWallet.owner)
            .filter(UserWallet.user == value)
            .count()
        )

        if user_wallet_counts == 10:
            raise HTTPException(400, {"message": "User can only have ten wallet!"})
        return value


class WalletDeposit(WalletBase):
    id: int


class WalletWithdraw(WalletBase):
    id: int


class Wallet(WalletBase):
    id: int
    title: str

    class Config:
        # Without orm_mode, if you returned a SQLAlchemy
        # model from your path operation,
        # it wouldn't include the relationship data
        orm_mode = True
