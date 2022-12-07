# Uvicorn Imports
import uvicorn

# Own Imports
from config.database import db_connect

# Routers Imports
from users.api import router as api_router
from users.auth import router as auth_router
from ledger.api import router as ledger_router

# FastAPI Imports
from fastapi import FastAPI


# Initialize fastapi
app = FastAPI(
    title="Ledger System",
    description="A fintech backend ledger system built with FastAPI.",
    version=1.0,
)

# Include routers to base router
app.include_router(api_router, tags=["Users"])
app.include_router(auth_router, tags=["Auth"])
app.include_router(ledger_router, tags=["Ledger"])


@app.on_event("startup")
async def startup():
    await db_connect.connect()


@app.on_event("shutdown")
async def disconnect():
    await db_connect.disconnect()


@app.get("/", tags=["Root"])
async def home() -> dict:
    """
    Ledger home

    Returns:
        dict: version and description
    """
    return {"v1": "Welcome to Ledger Fintech!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
