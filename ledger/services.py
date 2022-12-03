# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Own Imports
from ledger import schemas, models
from config.hashers import PasswordHasher


# Initialize password hasher
pwd_hasher = PasswordHasher()


def create_user(db: Session, user: schemas.UserCreate):

    hashed_password = pwd_hasher.hash_password(user.hashed_password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def create_wallet(db: Session, user_id: int, wallet: schemas.WalletCreate):

    db_wallet = models.Wallet(user=user_id, title=wallet.title, amount=wallet.amount)

    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)

    return db_wallet
