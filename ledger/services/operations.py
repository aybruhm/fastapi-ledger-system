# FastAPI Imports
from fastapi import HTTPException

# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Own Imports
from config.database import SessionLocal
from models.ledger import Wallet as UserWallet
from schemas.ledger import (
    Wallet2UserWalletTransfer,
    WalletWithdraw,
    WalletDeposit,
    Wallet2WalletTransfer,
)
from orm.ledger import ledger_orm
from orm.aggregate import ledger_aggregate_orm


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

    async def deposit_money_to_wallet(
        self, deposit: WalletDeposit
    ) -> UserWallet:
        """
        This function deposit x amount to the user wallet.

        :param deposit: schemas.WalletDeposit
        :type deposit: schemas.WalletDeposit
        """

        topup_wallet = ledger_orm.partial_filter(
            {"wallet_id": deposit.id, "user_id": deposit.user}
        )
        topup_wallet.amount += deposit.amount

        self.db.commit()
        self.db.refresh(topup_wallet, ["amount"])

    async def withdraw_money_from_wallet(
        self, withdraw: WalletWithdraw
    ) -> UserWallet:
        """
        The function withdraws x amount from the user wallet.

        :param withdraw: schemas.WalletWithdraw
        :type withdraw: schemas.WalletWithdraw
        """

        withdraw_wallet = ledger_orm.partial_filter(
            {"wallet_id": withdraw.id, "user_id": withdraw.user}
        )
        withdraw_wallet.amount -= withdraw.amount

        self.db.commit()
        self.db.refresh(withdraw_wallet, ["amount"])

    async def withdraw_from_to_wallet_transfer(
        self, withdraw: Wallet2WalletTransfer
    ) -> UserWallet:
        """
        This function is responsible for transferring x amount
        from wallet y to wallet z.

        :param withdraw: schemas.Wallet2WalletTransfer
        :type withdraw: schemas.Wallet2WalletTransfer
        """

        from_wallet = ledger_orm.partial_filter(
            {"wallet_id": withdraw.wallet_from, "user_id": withdraw.user}
        )
        to_wallet = ledger_orm.partial_filter(
            {"wallet_id": withdraw.wallet_to, "user_id": withdraw.user}
        )

        from_wallet.amount -= withdraw.amount
        to_wallet.amount += withdraw.amount

        self.db.commit()
        self.db.refresh(from_wallet, ["amount"])
        self.db.refresh(to_wallet, ["amount"])

    async def withdraw_from_to_user_wallet_transfer(
        self, withdraw: Wallet2UserWalletTransfer
    ) -> UserWallet:
        """
        This function is responsible for transferring x amount
        from wallet y to user z wallet.

        :param withdraw: schemas.Wallet2UserWalletTransfer
        :type withdraw: schemas.Wallet2UserWalletTransfer

        :return: The to_wallet is being returned.
        """

        from_wallet = ledger_orm.partial_filter(
            {"wallet_id": withdraw.wallet_from, "user_id": withdraw.user}
        )
        to_wallet = ledger_orm.partial_filter(
            {"wallet_id": withdraw.wallet_to, "user_id": withdraw.user_to}
        )

        from_wallet.amount -= withdraw.amount
        to_wallet.amount += withdraw.amount

        self.db.commit()
        self.db.refresh(from_wallet, ["amount"])
        self.db.refresh(to_wallet, ["amount"])

        return to_wallet

    async def get_total_wallet_balance(self, user_id: int) -> int:
        """
        This function gets the total sum amomut of the user wallets.t

        :param user_id: The user id of the user whose wallets you want to get
        :type user_id: int

        :return: The total balance of all wallets for a user.
        """

        wallet = await ledger_aggregate_orm.total_sum(user_id)
        return wallet[0][0]

    async def get_wallet_balance(
        self, user_id: int, wallet_id: int
    ) -> UserWallet:
        """
        This function gets the balance of a single wallet.

        :param user_id: The user_id of the user who owns the wallet
        :type user_id: int

        :param wallet_id: The id of the wallet you want to get the balance of
        :type wallet_id: int

        :return: The balance of the wallet
        """

        wallet = await ledger_orm.get(user_id, wallet_id)
        return wallet


ledger_operations = LedgerOperations(SessionLocal)
