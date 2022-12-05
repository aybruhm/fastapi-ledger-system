# SQLAlchemy Imports
from sqlalchemy.orm import Session

# FastAPI Imports
from fastapi import HTTPException

# Own Imports
from ledger import schemas, models
from config.hashers import PasswordHasher


# Initialize password hasher
pwd_hasher = PasswordHasher()


def create_user(db: Session, user: schemas.UserCreate):
    """
    This function creates a new user in the database.
    
    :param db: Session
    :type db: Session
    
    :param user: schemas.UserCreate
    :type user: schemas.UserCreate
    
    :return: The user object
    """

    hashed_password = pwd_hasher.hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed_password)

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
    return db.query(models.User).filter(models.User.id == user_id).first()


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
    return db.query(models.User).offset(skip).limit(limit).all()


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
    return db.query(models.User).filter(models.User.email == user_email).first()


def create_wallet(db: Session, wallet: schemas.WalletCreate):
    """
    It creates a new wallet in the database.
    
    :param db: Session
    :type db: Session
    
    :param wallet: schemas.WalletCreate
    :type wallet: schemas.WalletCreate
    
    :return: The wallet that was created.
    """

    db_wallet = models.Wallet(
        title=wallet.title, user=wallet.user, amount=wallet.amount
    )

    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)

    return db_wallet


def get_all_wallets(db: Session, skip: int, limit: int):
    return db.query(models.Wallet).offset(skip).limit(limit).all()


def get_single_wallet(db: Session, user_id: int, wallet_id: int):
    """
    Get a single wallet from the database, otherwise; raise a HTTP Exception.
    
    :param db: Session
    :type db: Session
    
    :param user_id: The id of the user who owns the wallet
    :type user_id: int
    
    :param wallet_id: The id of the wallet we want to get
    :type wallet_id: int
    
    :return: The wallet that matches the user_id and wallet_id
    """
    db_wallet = (
        db.query(models.Wallet)
        .filter(models.User.id == user_id, models.Wallet.id == wallet_id)
        .first()
    )

    if db_wallet:
        return db_wallet
    raise HTTPException(400, {"message": "Wallet does not exist!"})


def deposit_money_to_wallet(db: Session, deposit: schemas.WalletDeposit):
    """
    This function takes a database session, a wallet deposit object, and returns a wallet object.
    
    :param db: Session
    :type db: Session
    
    :param deposit: schemas.WalletDeposit
    :type deposit: schemas.WalletDeposit
    
    :return: The wallet that has been topped up.
    """
    topup_wallet = get_single_wallet(db, deposit.user, deposit.id)
    topup_wallet.amount += deposit.amount

    db.commit()
    db.refresh(topup_wallet)

    return topup_wallet


def withdraw_money_from_wallet(db: Session, withdraw: schemas.WalletWithdraw):
    """
    The function takes a database session and a `WalletWithdraw` object as input. It then gets the
    wallet to withdraw from, subtracts the amount to withdraw from the wallet's balance, and returns the
    updated wallet.
    
    :param db: Session
    :type db: Session
    
    :param withdraw: schemas.WalletWithdraw
    :type withdraw: schemas.WalletWithdraw
    
    :return: The wallet that was just updated.
    """

    withdraw_wallet = get_single_wallet(db, withdraw.user, withdraw.id)
    withdraw_wallet.amount -= withdraw.amount

    db.commit()
    db.refresh(withdraw_wallet)

    return withdraw_wallet



