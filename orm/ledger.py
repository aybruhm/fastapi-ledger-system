# Own Imports
from orm.base import ORMSessionMixin, Session
from models.ledger import Wallet as Userwallet
from schemas.ledger import WalletCreate


class LedgerORM(ORMSessionMixin):
    """Ledger ORM responsible for interacting with the database."""

    skip: int = 0
    limit: int = 10

    def partial_list(self):
        """This method partially retrieves a list of the user wallets."""

        wallets = self.orm.query(Userwallet)
        return wallets

    def get(self, user_id: int, wallet_id: int):
        """This method retrives a wallet by its id and user/owner id."""

        wallet = (
            self.partial_list()
            .join(Userwallet.owner)
            .filter_by(
                Userwallet.user == user_id,
                Userwallet.id == wallet_id,
            )
            .first()
        )
        return wallet

    def list(self):
        """This method retrieves all the wallets in the database."""

        wallets = self.partial_list().all()
        return wallets

    def filter(self, **kwargs):
        """
        This method filters the list of of user wallets by:

        - the offset (default is 0)
        - the limit (default is 10)
        - the wallet owner/user id
        """

        wallets = (
            self.partial_list()
            .offset(self.skip if kwargs["skip"] is None else kwargs["skip"])
            .limit(self.limit if kwargs["limit"] is None else kwargs["limit"])
            .join(Userwallet.owner)
            .filter_by(Userwallet.user == kwargs["user_id"])
            .all()
        )
        return wallets

    def create(self, wallet: WalletCreate):
        """This method creates a new wallet."""

        user_wallet = Userwallet(**wallet.dict())

        self.orm.add(user_wallet)
        self.orm.commit()
        self.orm.refresh(user_wallet)

        return user_wallet

    def update(self, **kwargs):
        """This method updates a wallet."""

        wallet = self.orm.query(Userwallet).update(kwargs)

        self.orm.commit()
        self.orm.refresh(wallet)

        return wallet

    def delete(self, wallet_id: int):
        """This method deletes a wallet."""

        self.orm.query(Userwallet).filter_by(
            Userwallet.id == wallet_id
        ).delete()
        self.orm.commit()

        return True


ledger_orm = LedgerORM(Session)