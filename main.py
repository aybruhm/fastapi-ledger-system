# Uvicorn Imports
import uvicorn

# Own Imports
from ledger.api import app
from config.database import db_connect


@app.on_event("startup")
async def startup():
    await db_connect.connect()


@app.on_event("shutdown")
async def disconnect():
    await db_connect.disconnect()


if __name__ == "__main__":
    uvicorn.run("ledger.api:app", host="0.0.0.0", reload=True)
