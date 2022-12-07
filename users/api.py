# FastAPI Imports
from fastapi import APIRouter, Depends

# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Own Imports
from ledger import services
from core.constants import get_db

# Auth Imports
from auth.auth_bearer import JWTBearer

# Schemas Imports
from schemas.user import User


# Initialize jwt bearer and api router
jwt_bearer = JWTBearer()
router = APIRouter(dependencies=[Depends(jwt_bearer)], tags=["Users"])


@router.get("/users/", response_model=list[User])
async def users_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_users = services.get_users(db, skip, limit)
    return db_users


@router.get(
    "/users/me/",
    response_model=User,
)
async def user_info(user_id: int, db: Session = Depends(get_db)):
    db_user = services.get_user(db, user_id)
    return db_user
