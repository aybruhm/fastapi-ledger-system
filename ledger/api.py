# FastAPI Imports
from fastapi import APIRouter, Depends

# SQLAlchemy Imports
from sqlalchemy.orm import Session
from auth import hashers

# Services Imports
from ledger.services import (
    create_wallet,
    get_all_wallets,
    get_all_wallets_by_user,
    get_single_wallet,
    deposit_money_to_wallet,
    get_total_wallet_balance,
    get_wallet_balance,
    withdraw_from_to_user_wallet_transfer,
    withdraw_from_to_wallet_transfer,
    withdraw_money_from_wallet,
)
from users.services import create_user, get_user, get_user_by_email, get_users

# Core Imports
from core.constants import get_db

# Auth (Own) Imports
from auth.auth_handler import AuthHandler
from auth.auth_bearer import JWTBearer

# Schema Imports
from schemas.ledger import Wallet, WalletCreate, WalletDeposit, WalletWithdraw

# Config (Own) Imports
from config import database


# Initialize authentication, jwt_bearer and pwd_hasher
authentication = AuthHandler()
jwt_bearer = JWTBearer()
pwd_hasher = hashers.PasswordHasher()


# Initialze fastapi app
router = APIRouter(dependencies=[Depends(jwt_bearer)])


# models.Base.metadata.create_all(bind=database.DB_ENGINE)


@router.post(
    "/wallets/",
    response_model=Wallet,
)
def create_wallet(wallet: WalletCreate, db: Session = Depends(get_db)):
    db_wallet = create_wallet(db, wallet)
    return db_wallet


@router.get("/wallets/", response_model=list[Wallet])
def get_wallets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_wallets = get_all_wallets(db, skip, limit)
    return db_wallets


@router.post("/deposit/", dependencies=[Depends(jwt_bearer)])
async def deposit_money(deposit: WalletDeposit, db: Session = Depends(get_db)) -> dict:
    deposit_money_to_wallet(db, deposit)
    return {"message": f"NGN{deposit.amount} deposit successful!"}


@router.post("/withdraw/", dependencies=[Depends(jwt_bearer)])
async def withdraw_money(
    withdraw: WalletWithdraw, db: Session = Depends(get_db)
) -> dict:
    withdraw_money_from_wallet(db, withdraw)
    return {"message": f"NGN{withdraw.amount} withdrawn successful!"}


@router.post("/transfer/wallet-to-wallet/", dependencies=[Depends(jwt_bearer)])
async def wallet_to_wallet_transfer(
    wallet_from_id: int, withdraw: WalletWithdraw, db: Session = Depends(get_db)
) -> dict:
    withdraw_from_to_wallet_transfer(db, wallet_from_id, withdraw)
    return {
        "message": f"NGN{withdraw.amount} was transfered from W#{wallet_from_id} wallet to W#{withdraw.id} wallet!"
    }


@router.post("/transfer/wallet-to-user/", dependencies=[Depends(jwt_bearer)])
async def wallet_to_user_transfer(
    user_id: int,
    wallet_to_id: int,
    withdraw: WalletWithdraw,
    db: Session = Depends(get_db),
) -> dict:
    withdraw_from_to_user_wallet_transfer(db, user_id, wallet_to_id, withdraw)
    return {
        "message": f"Transferred NGN{withdraw.amount} to W#{wallet_to_id} U#{user_id} wallet."
    }


@router.get("/balance/", dependencies=[Depends(jwt_bearer)])
async def total_wallet_balance(
    skip: int = 0, limit: int = 100, user_id: int = None, db: Session = Depends(get_db)
) -> dict:
    balance = get_total_wallet_balance(db, skip, limit, user_id)
    return {"message": f"Total wallet balance is NGN{balance}"}


@router.get("/balance/wallet/", dependencies=[Depends(jwt_bearer)])
async def wallet_balance(
    user_id: int, wallet_id: int, db: Session = Depends(get_db)
) -> dict:
    balance = get_wallet_balance(db, user_id, wallet_id)
    return {"message": f"Wallet balance is NGN{balance}"}
