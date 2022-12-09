# Own Imports
from config.database import Base, DB_ENGINE


def create_db_and_tables():
    """create database tables"""
    
    Base.metadata.create_all(bind=DB_ENGINE)
