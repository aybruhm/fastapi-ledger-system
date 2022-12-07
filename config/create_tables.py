# Own Imports
from config.database import Base, DB_ENGINE


# create database tables
Base.metadata.create_all(bind=DB_ENGINE)
