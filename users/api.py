# FastAPI Imports
from fastapi import APIRouter, Depends, HTTPException

# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Core Imports
from core.constants import get_db, get_current_user

# Services Imports
from users.services import get_user, get_users

# Auth Imports
from auth.auth_bearer import JWTBearer

# Models Imports
from models.user import User as UserModel

# Schemas Imports
from schemas.user import User


# Initialize jwt bearer and api router
jwt_bearer = JWTBearer()
router = APIRouter(dependencies=[Depends(jwt_bearer)], tags=["Users"])


@router.get("/users/", response_model=list[User])
async def users_info(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    db_users = get_users(db, skip, limit)
    return db_users


@router.get("/users/me/", response_model=User)
async def user_info(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):

    if current_user.id != user_id:
        raise HTTPException(
            401, {"message": "Unauthorized to perform this action!"}
        )

    db_user = get_user(db, user_id)
    return db_user
