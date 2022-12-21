# Stdlib Imports
from typing import Union, List

# FastAPI Imports
from fastapi import HTTPException

# ORM Imports
from orm.ledger import ledger_orm
from schemas.ledger import WalletCreate
from models.ledger import Wallet as UserWallet
from orm.aggregate import ledger_aggregate_orm


def create_wallet(wallet: WalletCreate) -> UserWallet:
    """
    It creates a new wallet in the database.

    :param wallet: schemas.WalletCreate
    :type wallet: schemas.WalletCreate

    :return: The wallet that was created.
    """

    wallet = ledger_orm.create(wallet)
    return wallet


def get_all_wallets(skip: int, limit: int) -> List[UserWallet]:
    """
    This function gets all wallets from the database.

    :param skip: The number of records to skip
    :type skip: int

    :param limit: The maximum number of wallets to return
    :type limit: int

    :return: A list of all the wallets in the database.
    """
    return ledger_orm.list(skip, limit)


def get_all_wallets_by_user(skip: int, limit: int, user_id: int) -> List[UserWallet]:
    """
    This function gets all wallets for a user.

    :param skip: The number of records to skip
    :type skip: int

    :param limit: The maximum number of items to return
    :type limit: int

    :param user_id: The id of the user whose wallets you want to retrieve
    :type user_id: int

    :return: A list of all wallets for a given user.
    """
    return ledger_orm.filter(
        **{"skip": skip, "limit": limit, "user_id": user_id}
    )


def get_sum_of_all_wallets_by_user(user_id: int) -> int:
    """
    This function gets the sum of all wallets for user.

    :param user_id: The id of the user whose wallets you want to retrieve
    :type user_id: int

    :return : the sum of all wallets for a user
    """
    return ledger_aggregate_orm.total_sum(user_id)


def get_single_wallet(
    user_id: int, wallet_id: int
) -> Union[UserWallet, Exception]:
    """
    Get a single wallet from the database, otherwise; raise a HTTP Exception.

    :param user_id: The id of the user who owns the wallet
    :type user_id: int

    :param wallet_id: The id of the wallet we want to get
    :type wallet_id: int

    :return: The wallet that matches the user_id and wallet_id
    """
    wallet = ledger_orm.get(user_id, wallet_id)

    if wallet:
        return wallet
    raise HTTPException(400, {"message": "Wallet does not exist!"})
