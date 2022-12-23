# FastAPI Imports
from fastapi import APIRouter, Depends

# Own Imports
from auth.auth_bearer import jwt_bearer
from core.deps import get_db


# initialize router
router = APIRouter(
    dependencies=[
        Depends(jwt_bearer),
        Depends(get_db),
    ]
)
