# 3rd Party Imports
import jwt
from decouple import config

# FastAPI Imports
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

# Own Imports Imports
from auth.auth_bearer import JWTBearer
from config.database import SessionLocal
from users import services


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(JWTBearer())
):

    """
    This function takes a database session and a JWT token,
    and returns the user that the token belongs to.

    :param db: Session = Depends(get_db)
    :type db: Session

    :param token: str = Depends(JWTBearer())
    :type token: str

    :return: The user object.
    """
    try:
        payload = jwt.decode(
            token, config("JWT_SECRET"), algorithms=[config("JWT_ALGORITHM")]
        )
    except (jwt.PyJWTError, Exception):
        raise HTTPException(403, {"message": "Could not validate token."})

    user = services.get_user(db, payload["user_id"])
    if not user:
        raise HTTPException(404, {"message": "User does not exist!"})
    return user
