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