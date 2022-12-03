# FastAPI Imports
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def ledger_home() -> dict:
    """
    Ledger home

    Returns:
        dict: version and description
    """
    return {"v1": "Welcome to Ledger Fintech!"}


@app.post("/deposit/")
async def deposit_money() -> dict:
    return {}


@app.post("/withdraw/")
async def withdraw_money() -> dict:
    return {}


@app.post("/transfer/wallet-to-wallet/{wallet_from_id}/{wallet_to_id}/")
async def wallet_to_wallet_transfer(wallet_from_id: int, wallet_to_id: int) -> dict:
    return {}


@app.post("/transfer/wallet-to-user/{wallet_id}/{user_id}")
async def wallet_to_user_transfer(user_id: int) -> dict:
    return {}


@app.get("/balance/")
async def total_wallet_balance() -> dict:
    return {}


@app.get("/balance/wallet/{wallet_id}")
async def wallet_balance(wallet_id: int) -> dict:
    return {}
