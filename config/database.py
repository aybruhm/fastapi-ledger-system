# Stdlib Imports
import os

# SQLAlchemy Imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "sqlite:///./ledger.sqlite"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

DB_ENGINE = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
) # connect_args={"check_same_thread": False} is needed only for SQLite. 
# It's not needed for other databases.

# Construct a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=DB_ENGINE)

# Construct a base class for declarative class definitions.
Base = declarative_base()