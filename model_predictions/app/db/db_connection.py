# db_connection.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
DATABASE_URL = "postgresql://postgres:admin@localhost/forex_db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining models
Base = declarative_base()
