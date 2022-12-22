# FastAPI Imports
from fastapi import HTTPException

# Own Imports
from orm.users import users_orm
from users.router import router
from users.services import create_user
from auth.auth_handler import authentication
from auth.hashers import pwd_hasher
from schemas.user import User, UserCreate
from schemas.auth import UserLoginSchema


@router.post("/users/", response_model=User)
async def create_new_user(new_user: UserCreate):
    user = await users_orm.get_email(new_user.email)

    if user:
        raise HTTPException(404, {"message": "User already exists!"})
    return await create_user(new_user)


@router.post("/login/")
async def login_user(authenticate: UserLoginSchema):
    user = await users_orm.get_email(authenticate.email)

    if user:
        user_token = authentication.sign_jwt(user.id)

        if pwd_hasher.check_password(authenticate.password, user.password):
            return user_token

        raise HTTPException(401, {"message": "Password incorrect!"})
    raise HTTPException(400, {"message": "User does not exist!"})
