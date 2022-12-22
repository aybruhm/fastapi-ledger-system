# Uvicorn Imports
import uvicorn

# FastAPI Imports
from fastapi import FastAPI

# Own Imports
from config.database import db_connect
from core.settings import ledger_settings

# Routers Imports
from users.auth import router as auth_router
from users.api import router as users_router
from ledger.api import router as ledger_router


# Initialize fastapi
app = FastAPI(
    title=ledger_settings.TITLE,
    description=ledger_settings.DESCRIPTION,
    version=ledger_settings.API_VERSION,
    contact=ledger_settings.CONTACT,
    license_info=ledger_settings.LICENSE,
)

# Include routers to base router
app.include_router(auth_router)
app.include_router(users_router, tags=["Users"])
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
