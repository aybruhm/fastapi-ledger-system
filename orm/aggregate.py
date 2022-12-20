# SQLAlchemy Imports
from sqlalchemy import func

# Own Imports
from orm.ledger import BaseLedgerORM, Userwallet, Session


class LedgerAggregateORM(BaseLedgerORM):
    """ORM responsible for performing aggregate operations."""

    def total_sum(self, user_id: int, skip: int, limit: int):
        """This method aggregates the amount of a user wallet."""

        return (
            self.orm.query(Userwallet)
            .join(Userwallet.owner)
            .filter(Userwallet.user == user_id)
            .offset(skip)
            .limit(limit)
            .with_entities(func.sum(Userwallet.amount))
            .all()
        )


ledger_aggregate_orm = LedgerAggregateORM(Session)
