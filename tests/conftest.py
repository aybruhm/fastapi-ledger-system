# Stdlib Imports
import sys
import os

# SQLAlchemy Impprts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Own Imports
from models.user import Base

# Third Party Imports
import pytest


# this is to include backend dir in sys.path so that we can import from db, main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture()
def create_tables():
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.    
    yield
    Base.metadata.drop_all(engine)


def _get_test_db():
    session = SessionTesting()
    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()
