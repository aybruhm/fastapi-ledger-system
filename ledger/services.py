# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Own Imports
from ledger import schemas, models
from config.hashers import PasswordHasher


# Initialize password hasher
pwd_hasher = PasswordHasher()


def create_user(db: Session, user: schemas.UserCreate):

    hashed_password = pwd_hasher.hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int, limit: int):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def create_wallet(db: Session, wallet: schemas.WalletCreate):

    db_wallet = models.Wallet(
        title=wallet.title, user=wallet.user, amount=wallet.amount
    )

    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)

    return db_wallet


def get_all_wallets(db: Session, skip: int, limit: int):
    return db.query(models.Wallet).offset(skip).limit(limit).all()


def deposit_money_to_wallet(db: Session, wallet: schemas.WalletDeposit):

    return ...


def withdraw_money_from_wallet(db: Session, wallet: schemas.WalletWithdraw):

    return ...
