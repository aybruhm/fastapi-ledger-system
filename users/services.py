# Own Imports
from auth.hashers import pwd_hasher
from orm.users import users_orm
from schemas.user import UserCreate
from models.user import User


async def create_user(user: UserCreate) -> User:
    """
    This function creates a new user in the database.

    :param user: schemas.UserCreate
    :type user: schemas.UserCreate

    :return: The user object
    """

    hashed_password = pwd_hasher.hash_password(user.password)
    user = await users_orm.create(user, hashed_password)
    return user
