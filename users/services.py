# SQLAlchemy Imports
from sqlalchemy.orm import Session, joinedload

# Auth Imports
from auth.hashers import PasswordHasher

# Schemas Imports
from schemas.user import UserCreate

# Models Imports
from models.user import User


# Initialize password hasher
pwd_hasher = PasswordHasher()


def create_user(db: Session, user: UserCreate):
    """
    This function creates a new user in the database.

    :param db: Session
    :type db: Session

    :param user: schemas.UserCreate
    :type user: schemas.UserCreate

    :return: The user object
    """

    hashed_password = pwd_hasher.hash_password(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_email(db: Session, user_email: str):
    """
    This function gets a user from the database by their email address.

    :param db: Session
    :type db: Session

    :param user_email: The email address of the user you want to get
    :type user_email: str

    :return: The first user in the database with the email 
    address that matches the user_email
    parameter.
    """
    return (
        db.query(User)
        .options(joinedload(User.wallets))
        .filter(User.email == user_email)
        .first()
    )
