# FastAPI Imports
from fastapi import FastAPI, Depends, HTTPException

# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Own Imports
from ledger import models, schemas, services
from ledger.constants import get_db
from config import database


app = FastAPI(
    title="Ledger System",
    description="A fintech backend ledger system built with FastAPI.",
    version=1.0,
)
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


@app.get("/users/", response_model=list[schemas.User], tags=["Users"])
async def users_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_users = services.get_users(db, skip, limit)
    return db_users


@app.get("/users/{user_id}/", response_model=schemas.User, tags=["Users"])
async def user_info(user_id: int, db: Session = Depends(get_db)):
    db_user = services.get_user(db, user_id)
    return db_user


@app.post("/deposit/", tags=["Ledger"])
async def deposit_money() -> dict:
    return {}


@app.post("/withdraw/", tags=["Ledger"])
async def withdraw_money() -> dict:
    return {}


@app.post(
    "/transfer/wallet-to-wallet/{wallet_from_id}/{wallet_to_id}/", tags=["Ledger"]
)
async def wallet_to_wallet_transfer(wallet_from_id: int, wallet_to_id: int) -> dict:
    return {}


@app.post("/transfer/wallet-to-user/{wallet_id}/{user_id}", tags=["Ledger"])
async def wallet_to_user_transfer(user_id: int) -> dict:
    return {}


@app.get("/balance/", tags=["Ledger"])
async def total_wallet_balance() -> dict:
    return {}


@app.get("/balance/wallet/{wallet_id}", tags=["Ledger"])
async def wallet_balance(wallet_id: int) -> dict:
    return {}
