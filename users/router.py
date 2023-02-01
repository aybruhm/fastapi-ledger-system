# FastAPI Imports
from fastapi import APIRouter, Depends

# Own Imports
from auth.auth_bearer import jwt_bearer


# initialize router
router = APIRouter(dependencies=[Depends(jwt_bearer)])
