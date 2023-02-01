# Stdlib Imports
import sys
import os
import warnings

# SQLAlchemy Impprts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Own Imports
from models.user import Base

# Third Party Imports
import pytest
import alembic
from alembic.config import Config


# this is to include backend dir in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite"

# Create Database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """
    This function creates all the tables in the database,
    then drops them.
    """

    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def _get_test_db():

    # Call method to create tables
    create_tables()

    session = SessionTesting()
    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()
