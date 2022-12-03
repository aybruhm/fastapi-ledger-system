# Uvicorn Imports
import uvicorn



if __name__ == "__main__":
    uvicorn.run("ledger.api:app", host="0.0.0.0", reload=True)