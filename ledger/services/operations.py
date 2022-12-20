# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Schemas Imports
from models.ledger import Wallet as UserWallet
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

    def __init__(self, db: Session):
        self.db = db

    def deposit_money_to_wallet(self, deposit: WalletDeposit) -> UserWallet:
        """
        This function deposit x amount to the user wallet.

        :param deposit: schemas.WalletDeposit
        :type deposit: schemas.WalletDeposit

        :return: The wallet that has been topped up.
        """

        topup_wallet = get_single_wallet(deposit.user, deposit.id)
        topup_wallet.amount += deposit.amount

        self.db.commit()
        self.db.refresh(topup_wallet)

        return topup_wallet

    def withdraw_money_from_wallet(
        self, withdraw: WalletWithdraw
    ) -> UserWallet:
        """
        The function withdraws x amount from the user wallet.

        :param withdraw: schemas.WalletWithdraw
        :type withdraw: schemas.WalletWithdraw

        :return: The wallet that was just updated.
        """

        withdraw_wallet = get_single_wallet(withdraw.user, withdraw.id)
        withdraw_wallet.amount -= withdraw.amount

        self.db.commit()
        self.db.refresh(withdraw_wallet)

        return withdraw_wallet

    def withdraw_from_to_wallet_transfer(
        self, from_wallet_id: int, withdraw: WalletWithdraw
    ) -> UserWallet:
        """
        This function is responsible for transferring x amount from wallet y to wallet z.

        :param from_wallet_id: The wallet id of the wallet you want to withdraw from
        :type from_wallet_id: int

        :param withdraw: schemas.WalletWithdraw
        :type withdraw: schemas.WalletWithdraw

        :return: The to_wallet is being returned.
        """

        from_wallet = get_single_wallet(withdraw.user, from_wallet_id)
        to_wallet = get_single_wallet(withdraw.user, withdraw.id)

        from_wallet.amount -= withdraw.amount
        to_wallet.amount += withdraw.amount

        self.db.commit()
        self.db.refresh(from_wallet)
        self.db.refresh(to_wallet)

        return to_wallet

    def withdraw_from_to_user_wallet_transfer(
        self, user_id: int, wallet_to: int, withdraw: WalletWithdraw
    ) -> UserWallet:
        """
        This function is responsible for transferring x amount from wallet y to user z wallet.

        :param from_wallet_id: The wallet id of the wallet you want to withdraw from
        :type from_wallet_id: int

        :param withdraw: schemas.WalletWithdraw
        :type withdraw: schemas.WalletWithdraw

        :return: The to_wallet is being returned.
        """

        from_wallet = get_single_wallet(withdraw.user, withdraw.id)
        to_wallet = get_single_wallet(user_id, wallet_to)

        from_wallet.amount -= withdraw.amount
        to_wallet.amount += withdraw.amount

        self.db.commit()
        self.db.refresh(from_wallet)
        self.db.refresh(to_wallet)

        return to_wallet

    def get_total_wallet_balance(
        self, user_id: int
    ) -> int:
        """
        This function gets the total sum amomut of the user wallets.t

        :param user_id: The user id of the user whose wallets you want to get
        :type user_id: int

        :return: The total balance of all wallets for a user.
        """

        wallet = get_sum_of_all_wallets_by_user(user_id)
        return wallet[0][0]

    def get_wallet_balance(self, user_id: int, wallet_id: int) -> int:
        """
        This function gets the balance of a single wallet.

        :param user_id: The user_id of the user who owns the wallet
        :type user_id: int

        :param wallet_id: The id of the wallet you want to get the balance of
        :type wallet_id: int

        :return: The balance of the wallet
        """

        wallet = get_single_wallet(user_id, wallet_id)
        return wallet.amount


ledger_operations = LedgerOperations(Session)
