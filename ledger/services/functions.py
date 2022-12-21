# Stdlib Imports
from typing import List

# ORM Imports
from orm.ledger import ledger_orm
from schemas.ledger import WalletCreate
from models.ledger import Wallet as UserWallet


async def create_wallet(wallet: WalletCreate) -> UserWallet:
    """
    It creates a new wallet in the database.

    :param wallet: schemas.WalletCreate
    :type wallet: schemas.WalletCreate

    :return: The wallet that was created.
    """

    wallet = await ledger_orm.create(wallet)
    return wallet


async def get_all_wallets_by_user(
    skip: int, 
    limit: int, 
    user_id: int
) -> List[UserWallet]:
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
    return await ledger_orm.filter(
        **{"skip": skip, "limit": limit, "user_id": user_id}
    )
