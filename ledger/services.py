# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Own Imports
from ledger import schemas, models
from config.hashers import PasswordHasher


# Initialize password hasher
pwd_hasher = PasswordHasher()


def create_user(db: Session, user: schemas.UserCreate):
    # Hash user password
    hashed_password = pwd_hasher.hash_password(user.hashed_password)

    # Create user
    db_user = models.User(email=user.email, hashed_password=hashed_password)

    # Add, commmit and refresh database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Return user
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()
