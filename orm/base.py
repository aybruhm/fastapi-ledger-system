# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Own Imports
from config.database import SessionLocal
from tests.conftest import _get_test_db
from core.settings import ledger_settings


class ORMSessionMixin:
    """Base orm session mixin for interacting with the database."""

    def __init__(self):
        """
        If we're not using the test database, then get the next database session from the database pool.
        Otherwise, get the next database session from the test database pool.
        """
        self.orm: Session = (
            self.get_db().__next__()
            if not ledger_settings.USE_TEST_DB
            else _get_test_db().__next__()
        )

    def get_db(self):
        """
        This function creates a database session,
        yield it to the get_db function, rollback the transaction
        if there's an exception and then finally closes the session.

        Yields:
            db: scoped database session
        """
        db = SessionLocal()
        try:
            yield db
        except Exception:
            db.rollback()
        finally:
            db.close()
