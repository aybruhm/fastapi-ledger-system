# SQLAlchemy Imports
from sqlalchemy import func

# Own Imports
from orm.ledger import BaseLedgerORM, Userwallet, SessionLocal


class LedgerAggregateORM(BaseLedgerORM):
    """ORM responsible for performing aggregate operations."""

    def total_sum(self, user_id: int):
        """This method aggregates the amount of a user wallet."""

        return (
            self.orm.query(Userwallet)
            .join(Userwallet.owner)
            .filter(Userwallet.user == user_id)
            .with_entities(func.sum(Userwallet.amount))
            .all()
        )


ledger_aggregate_orm = LedgerAggregateORM(SessionLocal())
