# Uvicorn Imports
import uvicorn



if __name__ == "__main__":
    uvicorn.run("ledger.api:ledger", host="0.0.0.0", reload=True)