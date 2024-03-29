# Stdlib Imports
import os

# SQLAlchemy Imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Third Party Imports
from databases import Database


# SQLALCHEMY_DATABASE_URL = "sqlite:///./ledger.sqlite"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

DB_ENGINE = create_engine(
    SQLALCHEMY_DATABASE_URL
)  # connect_args={"check_same_thread": False} is needed only for SQLite.
# It's not needed for other databases.

# Construct a session maker
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=DB_ENGINE)
SessionLocal = scoped_session(session_factory)

# Construct a base class for declarative class definitions.
Base = declarative_base()

# Construct a db connector to connect, shutdown database
db_connect = Database(SQLALCHEMY_DATABASE_URL)
