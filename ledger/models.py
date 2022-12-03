# SQLAlchemy Imports
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Own Imports
from config.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    wallets = relationship("Wallet", back_populates="owner")
    
    
class Wallet(Base):
    __tablename__ = "users_wallet"
    
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    amount = Column(Integer, default=0)
    