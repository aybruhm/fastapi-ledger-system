# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Schemas Imports
from schemas.ledger import WalletWithdraw, WalletDeposit
from ledger.services.functions import (
    get_single_wallet,
    get_sum_of_all_wallets_by_user,
)


class LedgerOperations:
    """
    This service is responsible for:
    
    - depositing money to wallet
    - withdrawing money from wallet
    - wallet to wallet withdraw transfer
    - wallet to user wallet transfer
    - get total wallet balance
    - get wallet balance
    """
    
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

    def get_total_wallet_balance(
        db: Session, skip: int, limit: int, user_id: int
    ):
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


ledger_operations = LedgerOperations()