# Stdlib Imports
import datetime

# SQLAlchemy Imports
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

# Config Imports
from config.database import Base

# Wallet Imports
from models.ledger import Wallet


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    wallets = relationship(Wallet, back_populates="owner")
