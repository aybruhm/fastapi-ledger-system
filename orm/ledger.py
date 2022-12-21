# Stdlib Imports
from typing import List

# Own Imports
from orm.base import ORMSessionMixin
from schemas.ledger import WalletCreate
from config.database import SessionLocal
from models.ledger import Wallet as Userwallet


class BaseLedgerORM(ORMSessionMixin):
    """Base Ledger ORM responsible for interacting with the database."""

    skip: int = 0
    limit: int = 10

    def partial_list(self):
        """This method partially retrieves a list of the user wallets."""

        wallets = self.orm.query(Userwallet)
        return wallets


class LedgerORM(BaseLedgerORM):
    """CRUD Operations for the ledger to interact with the database."""

    async def get(self, user_id: int, wallet_id: int) -> Userwallet:
        """This method retrives a wallet by its id and user/owner id."""

        wallet = (
            self.partial_list()
            .join(Userwallet.owner)
            .filter(Userwallet.user == user_id)
            .filter(Userwallet.id == wallet_id)
            .first()
        )
        return wallet

    async def list(self, skip: int, limit: int) -> List[Userwallet]:
        """This method retrieves all the wallets in the database."""

        wallets = (
            self.partial_list()
            .offset(self.skip if skip is None else skip)
            .limit(self.limit if limit is None else limit)
            .all()
        )
        return wallets

    async def filter(self, **kwargs) -> List[Userwallet]:
        """
        This method filters the list of of user wallets by:

        - the offset (default is 0)
        - the limit (default is 10)
        - the wallet owner/user id
        """

        wallets = (
            self.partial_list()
            .join(Userwallet.owner)
            .filter(Userwallet.user == kwargs["user_id"])
            .offset(self.skip if kwargs["skip"] is None else kwargs["skip"])
            .limit(self.limit if kwargs["limit"] is None else kwargs["limit"])
            .all()
        )
        return wallets

    async def create(self, wallet: WalletCreate) -> Userwallet:
        """This method creates a new wallet."""

        user_wallet = Userwallet(**wallet.dict())

        self.orm.add(user_wallet)
        self.orm.commit()
        self.orm.refresh(user_wallet)

        return user_wallet

    async def update(self, **kwargs) -> Userwallet:
        """This method updates a wallet."""

        wallet = self.orm.query(Userwallet).update(kwargs)

        self.orm.commit()
        self.orm.refresh(wallet)

        return wallet

    async def delete(self, wallet_id: int) -> bool:
        """This method deletes a wallet."""

        self.orm.query(Userwallet).filter_by(
            Userwallet.id == wallet_id
        ).delete()
        self.orm.commit()

        return True


ledger_orm = LedgerORM(SessionLocal())
