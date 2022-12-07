# Stdlib Imports
import datetime

# SQLAlchemy Imports
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

# Core Imports
from config.database import Base


class Wallet(Base):
    __tablename__ = "users_wallet"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    amount = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    owner = relationship("User", back_populates="wallets")
