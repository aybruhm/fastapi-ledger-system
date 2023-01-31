# FastAPI Imports
from fastapi import Depends, HTTPException

# Own Imports Imports
from models.user import User
from orm.users import users_orm
from auth.auth_bearer import jwt_bearer

# 3rd Party Imports
import jwt
from decouple import config


async def get_current_user(token: str = Depends(jwt_bearer)) -> User:
    """
    This function takes a JWT token,
    and returns the user that the token belongs to.

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

    user = await users_orm.get(payload["user_id"])
    if not user:
        raise HTTPException(404, {"message": "User does not exist!"})
    return user


async def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    This function returns an admin user based on the provided token;
    otherwise, raise an authorized exception.
    """

    if not current_user.is_admin:
        raise HTTPException(401, {"message": "Admin priviledge is required!"})

    elif current_user is None:
        return None

    return current_user
