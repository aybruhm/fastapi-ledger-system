# Stdlib Imports
import datetime

# SQLAlchemy Imports
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

# Own Imports
from config.database import Base


# NOTE:
# -------
# When accessing the attribute wallets in a User, as in my_user.wallets, 
# it will have a list of Wallet SQLAlchemy models (from the users_wallet table) that 
# have a foreign key pointing to this record in the users table.

# When you access my_user.wallets, SQLAlchemy will actually go and fetch the wallets 
# from the database in the users_wallet table and populate them here.

# And when accessing the attribute owner in an Wallet, it will contain a User 
# SQLAlchemy model from the users table. It will use the owner_id attribute/column 
# with its foreign key to know which record to get from the users table.


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    wallets = relationship("Wallet", back_populates="owner")


class Wallet(Base):
    __tablename__ = "users_wallet"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    amount = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    
    
    owner = relationship("User", back_populates="wallets")
