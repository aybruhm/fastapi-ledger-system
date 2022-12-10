# SQLAlchemy Imports
from sqlalchemy.orm import Session
from sqlalchemy import func

# FastAPI Imports
from fastapi import HTTPException

# Schemas Imports
from schemas.ledger import WalletCreate, WalletWithdraw, WalletDeposit

# Models Imports
from models.user import User
from models.ledger import Wallet as UserWallet


def create_wallet(db: Session, wallet: WalletCreate):
    """
    It creates a new wallet in the database.

    :param db: Session
    :type db: Session

    :param wallet: schemas.WalletCreate
    :type wallet: schemas.WalletCreate

    :return: The wallet that was created.
    """

    db_wallet = UserWallet(
        title=wallet.title, user=wallet.user, amount=wallet.amount
    )

    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)

    return db_wallet


def get_all_wallets(db: Session, skip: int, limit: int):
    """
    This function gets all wallets from the database.

    :param db: Session: This is the database session that we created in the previous section
    :type db: Session

    :param skip: The number of records to skip
    :type skip: int

    :param limit: The maximum number of wallets to return
    :type limit: int

    :return: A list of all the wallets in the database.
    """
    return db.query(UserWallet).offset(skip).limit(limit).all()


def get_all_wallets_by_user(db: Session, skip: int, limit: int, user_id: int):
    """
    This function gets all wallets for a user.

    :param db: Session - the database session
    :type db: Session

    :param skip: The number of records to skip
    :type skip: int

    :param limit: The maximum number of items to return
    :type limit: int

    :param user_id: The id of the user whose wallets you want to retrieve
    :type user_id: int

    :return: A list of all wallets for a given user.
    """
    return (
        db.query(UserWallet)
        .join(UserWallet.owner)
        .filter(User.id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_sum_of_all_wallets_by_user(
    db: Session, skip: int, limit: int, user_id: int
):
    """
    This function gets the sum of all wallets for user.

    :param db: Session - the database session
    :type db: Session

    :param skip: The number of records to skip
    :type skip: int

    :param limit: The maximum number of items to return
    :type limit: int

    :param user_id: The id of the user whose wallets you want to retrieve
    :type user_id: int

    :return : the sum of all wallets for a user
    """
    return (
        db.query(UserWallet)
        .join(UserWallet.owner)
        .filter(User.id == user_id)
        .offset(skip)
        .limit(limit)
        .with_entities(func.sum(UserWallet.amount))
        .all()
    )


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
        db.query(UserWallet)
        .join(UserWallet.owner)
        .filter(User.id == user_id)
        .filter(UserWallet.id == wallet_id)
        .first()
    )

    if db_wallet:
        return db_wallet
    raise HTTPException(400, {"message": "Wallet does not exist!"})


def deposit_money_to_wallet(db: Session, deposit: WalletDeposit):
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


def withdraw_money_from_wallet(db: Session, withdraw: WalletWithdraw):
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


def withdraw_from_to_wallet_transfer(
    db: Session, from_wallet_id: int, withdraw: WalletWithdraw
):
    """
    This function is responsible for transferring x amount from wallet y to wallet z.

    :param db: Session, from_wallet_id: int, withdraw: schemas.WalletWithdraw
    :type db: Session

    :param from_wallet_id: The wallet id of the wallet you want to withdraw from
    :type from_wallet_id: int

    :param withdraw: schemas.WalletWithdraw
    :type withdraw: schemas.WalletWithdraw

    :return: The to_wallet is being returned.
    """

    from_wallet = get_single_wallet(db, withdraw.user, from_wallet_id)
    to_wallet = get_single_wallet(db, withdraw.user, withdraw.id)

    from_wallet.amount -= withdraw.amount
    to_wallet.amount += withdraw.amount

    db.commit()
    db.refresh(from_wallet)
    db.refresh(to_wallet)

    return to_wallet


def withdraw_from_to_user_wallet_transfer(
    db: Session, user_id: int, wallet_to: int, withdraw: WalletWithdraw
):
    """
    This function is responsible for transferring x amount from wallet y to user z wallet.

    :param db: Session, from_wallet_id: int, withdraw: schemas.WalletWithdraw
    :type db: Session

    :param from_wallet_id: The wallet id of the wallet you want to withdraw from
    :type from_wallet_id: int

    :param withdraw: schemas.WalletWithdraw
    :type withdraw: schemas.WalletWithdraw

    :return: The to_wallet is being returned.
    """

    from_wallet = get_single_wallet(db, withdraw.user, withdraw.id)
    to_wallet = get_single_wallet(db, user_id, wallet_to)

    from_wallet.amount -= withdraw.amount
    to_wallet.amount += withdraw.amount

    db.commit()
    db.refresh(from_wallet)
    db.refresh(to_wallet)

    return to_wallet


def get_total_wallet_balance(db: Session, skip: int, limit: int, user_id: int):
    """
    This function gets all wallets for a user, then sum up the amount of each wallet.

    :param db: Session - this is the database session that we created in the previous step
    :type db: Session

    :param skip: the number of records to skip
    :type skip: int

    :param limit: The number of wallets to return
    :type limit: int

    :param user_id: The user id of the user whose wallets you want to get
    :type user_id: int

    :return: The total balance of all wallets for a user.
    """

    wallet = get_sum_of_all_wallets_by_user(db, skip, limit, user_id)
    return wallet[0][0]


def get_wallet_balance(db: Session, user_id: int, wallet_id: int):
    """
    This function gets the balance of a single wallet.

    :param db: Session - this is the database session that we created in the main.py file
    :type db: Session

    :param user_id: The user_id of the user who owns the wallet
    :type user_id: int

    :param wallet_id: The id of the wallet you want to get the balance of
    :type wallet_id: int

    :return: The balance of the wallet
    """

    wallet = get_single_wallet(db, user_id, wallet_id)
    balance = wallet.amount
    return balance
