# SQLAlchemy Imports
from sqlalchemy.orm import Session


class ORMSessionMixin:
    """Base orm session mixin for interacting with the database."""

    def __init__(self, orm: Session):
        self.orm = orm
