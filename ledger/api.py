# Stdlib Imports
import json

# FastAPI Imports
from fastapi import FastAPI, Depends, HTTPException

# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Own Imports
from ledger import models, schemas, services
from ledger.constants import get_db

# Auth (Own) Imports
from auth.auth_handler import AuthHandler
from auth.auth_bearer import JWTBearer
from auth.schemas import UserLoginSchema

# Config (Own) Imports
from config import database, hashers


app = FastAPI(
    title="Ledger System",
    description="A fintech backend ledger system built with FastAPI.",
    version=1.0,
)
authentication = AuthHandler()
pwd_hasher = hashers.PasswordHasher()


models.Base.metadata.create_all(bind=database.DB_ENGINE)


@app.get("/", tags=["Root"])
async def ledger_home() -> dict:
    """
    Ledger home

    Returns:
        dict: version and description
    """
    return {"v1": "Welcome to Ledger Fintech!"}


@app.post("/users/", response_model=schemas.User, tags=["Users"])
async def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, user.email)

    if db_user:
        raise HTTPException(400, {"message": "User already exists!"})
    return services.create_user(db, user=user)


@app.post("/login/", tags=["Auth"])
async def login_user(user: UserLoginSchema, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, user.email)

    if db_user:
        user_token = authentication.sign_jwt(db_user.id)

        if pwd_hasher.check_password(user.password, db_user.password):
            return user_token

        raise HTTPException(401, {"message": "Password incorrect!"})
    raise HTTPException(400, {"message": "User does not exist!"})


@app.get("/users/", response_model=list[schemas.User], tags=["Users"])
async def users_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_users = services.get_users(db, skip, limit)
    return db_users


@app.get(
    "/users/{user_id}/",
    dependencies=[Depends(JWTBearer())],
    response_model=schemas.User,
    tags=["Users"],
)
async def user_info(user_id: int, db: Session = Depends(get_db)):
    db_user = services.get_user(db, user_id)
    return db_user


@app.post(
    "/wallets/",
    dependencies=[Depends(JWTBearer())],
    response_model=schemas.Wallet,
    tags=["Ledger"],
)
def create_wallet(wallet: schemas.WalletCreate, db: Session = Depends(get_db)):
    db_wallet = services.create_wallet(db, wallet)
    return db_wallet


@app.get("/wallets/", response_model=list[schemas.Wallet], tags=["Ledger"])
def get_wallets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_wallets = services.get_all_wallets(db, skip, limit)
    return db_wallets


@app.post("/deposit/", dependencies=[Depends(JWTBearer())], tags=["Ledger"])
async def deposit_money(
    deposit: schemas.WalletDeposit, db: Session = Depends(get_db)
) -> dict:
    services.deposit_money_to_wallet(db, deposit)
    return {"message": f"NGN{deposit.amount} deposit successful!"}


@app.post("/withdraw/", dependencies=[Depends(JWTBearer())], tags=["Ledger"])
async def withdraw_money(
    withdraw: schemas.WalletWithdraw, db: Session = Depends(get_db)
) -> dict:
    services.withdraw_money_from_wallet(db, withdraw)
    return {"message": f"NGN{withdraw.amount} withdrawn successful!"}


@app.post(
    "/transfer/wallet-to-wallet/", dependencies=[Depends(JWTBearer())], tags=["Ledger"]
)
async def wallet_to_wallet_transfer(
    wallet_from_id: int, withdraw: schemas.WalletWithdraw, db: Session = Depends(get_db)
) -> dict:
    services.withdraw_from_to_wallet_transfer(db, wallet_from_id, withdraw)
    return {
        "message": f"NGN{withdraw.amount} was transfered from W#{wallet_from_id} wallet to W#{withdraw.id} wallet!"
    }


@app.post(
    "/transfer/wallet-to-user/", dependencies=[Depends(JWTBearer())], tags=["Ledger"]
)
async def wallet_to_user_transfer(
    user_id: int,
    wallet_to_id: int,
    withdraw: schemas.WalletWithdraw,
    db: Session = Depends(get_db),
) -> dict:
    services.withdraw_from_to_user_wallet_transfer(db, user_id, wallet_to_id, withdraw)
    return {
        "message": f"Transferred NGN{withdraw.amount} to W#{wallet_to_id} U#{user_id} wallet."
    }


@app.get("/balance/", dependencies=[Depends(JWTBearer())], tags=["Ledger"])
async def total_wallet_balance(
    skip: int = 0, limit: int = 100, user_id: int = None, db: Session = Depends(get_db)
) -> dict:
    balance = services.get_total_wallet_balance(db, skip, limit, user_id)
    return {"message": f"Total wallet balance is NGN{balance}"}


@app.get("/balance/wallet/", dependencies=[Depends(JWTBearer())], tags=["Ledger"])
async def wallet_balance(
    user_id: int, wallet_id: int, db: Session = Depends(get_db)
) -> dict:
    balance = services.get_wallet_balance(db, user_id, wallet_id)
    return {"message": f"Wallet balance is NGN{balance}"}
