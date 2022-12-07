# SQLAlchemy Imports
from sqlalchemy.orm import Session, joinedload

# Auth Imports
from auth.hashers import PasswordHasher

# Models Imports
from schemas.user import User, UserCreate


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


def get_user(db: Session, user_id: int):
    """
    This function gets a user from the database by ID.

    :param db: Session
    :type db: Session

    :param user_id: The ID of the user to get
    :type user_id: int

    :return: The first user in the database with the id of user_id
    """
    return (
        db.query(User)
        .options(joinedload(User.wallets))
        .filter(User.id == user_id)
        .first()
    )


def get_users(db: Session, skip: int, limit: int):
    """
    This function gets all users from the database,
    skipping the first `skip` users, and limiting
    the result to `limit` users.

    :param db: Session
    :type db: Session

    :param skip: The number of records to skip
    :type skip: int

    :param limit: The number of items to return
    :type limit: int

    :return: A list of users
    """
    return (
        db.query(User)
        .options(joinedload(User.wallets))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_user_by_email(db: Session, user_email: str):
    """
    This function gets a user from the database by their email address.

    :param db: Session
    :type db: Session

    :param user_email: The email address of the user you want to get
    :type user_email: str

    :return: The first user in the database with the email address that matches the user_email
    parameter.
    """
    return (
        db.query(User)
        .options(joinedload(User.wallets))
        .filter(User.email == user_email)
        .first()
    )
