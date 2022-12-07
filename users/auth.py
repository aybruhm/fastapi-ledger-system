# FastAPI Imports
from fastapi import APIRouter, Depends, HTTPException

# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Own Imports
from ledger import services
from core.constants import get_db

# Auth Imports
from auth.auth_handler import AuthHandler
from auth.hashers import PasswordHasher

# Schemas Imports
from schemas.user import User, UserCreate
from schemas.auth import UserLoginSchema


# Initialize api router,
# auth handler, and password hasher
router = APIRouter()
auth_handler = AuthHandler()
pwd_hasher = PasswordHasher()


@router.post("/users/", response_model=User)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, user.email)

    if db_user:
        raise HTTPException(400, {"message": "User already exists!"})
    return services.create_user(db, user=user)


@router.post("/login/", tags=["Auth"])
async def login_user(user: UserLoginSchema, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, user.email)

    if db_user:
        user_token = auth_handler.sign_jwt(db_user.id)

        if pwd_hasher.check_password(user.password, db_user.password):
            return user_token

        raise HTTPException(401, {"message": "Password incorrect!"})
    raise HTTPException(400, {"message": "User does not exist!"})
