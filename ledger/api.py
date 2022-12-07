# FastAPI Imports
from fastapi import APIRouter, Depends

# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Services Imports
from ledger.services import (
    create_wallet as create_user_wallet,
    get_all_wallets,
    deposit_money_to_wallet,
    get_total_wallet_balance,
    get_wallet_balance,
    withdraw_from_to_user_wallet_transfer,
    withdraw_from_to_wallet_transfer,
    withdraw_money_from_wallet,
)

# Core Imports
from core.constants import get_db

# Auth (Own) Imports
from auth.auth_handler import AuthHandler
from auth.auth_bearer import JWTBearer
from auth.hashers import PasswordHasher

# Schema Imports
from schemas.ledger import Wallet, WalletCreate, WalletDeposit, WalletWithdraw


# Initialize authentication, jwt_bearer and pwd_hasher
authentication = AuthHandler()
jwt_bearer = JWTBearer()
pwd_hasher = PasswordHasher()


# Initialze fastapi app
router = APIRouter(dependencies=[Depends(jwt_bearer)])


@router.post("/wallets/", response_model=Wallet)
async def create_wallet(wallet: WalletCreate, db: Session = Depends(get_db)):
    db_wallet = create_user_wallet(db, wallet)
    return db_wallet


@router.get("/wallets/", response_model=list[Wallet])
async def get_wallets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_wallets = get_all_wallets(db, skip, limit)
    return db_wallets


@router.post("/deposit/")
async def deposit_money(deposit: WalletDeposit, db: Session = Depends(get_db)) -> dict:
    deposit_money_to_wallet(db, deposit)
    return {"message": f"NGN{deposit.amount} deposit successful!"}


@router.post("/withdraw/")
async def withdraw_money(
    withdraw: WalletWithdraw, db: Session = Depends(get_db)
) -> dict:
    withdraw_money_from_wallet(db, withdraw)
    return {"message": f"NGN{withdraw.amount} withdrawn successful!"}


@router.post("/transfer/wallet-to-wallet/")
async def wallet_to_wallet_transfer(
    wallet_from_id: int, withdraw: WalletWithdraw, db: Session = Depends(get_db)
) -> dict:
    withdraw_from_to_wallet_transfer(db, wallet_from_id, withdraw)
    return {
        "message": f"NGN{withdraw.amount} was transfered from W#{wallet_from_id} wallet to W#{withdraw.id} wallet!"
    }


@router.post("/transfer/wallet-to-user/")
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


@router.get("/balance/")
async def total_wallet_balance(
    skip: int = 0, limit: int = 100, user_id: int = None, db: Session = Depends(get_db)
) -> dict:
    balance = get_total_wallet_balance(db, skip, limit, user_id)
    return {"message": f"Total wallet balance is NGN{balance}"}


@router.get("/balance/wallet/")
async def wallet_balance(
    user_id: int, wallet_id: int, db: Session = Depends(get_db)
) -> dict:
    balance = get_wallet_balance(db, user_id, wallet_id)
    return {"message": f"Wallet balance is NGN{balance}"}
