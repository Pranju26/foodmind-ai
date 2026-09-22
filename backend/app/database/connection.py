import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# The engine manages the actual connection to PostgreSQL
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory that creates new database sessions when needed
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is what all our table models will inherit from
Base = declarative_base()


# This function provides a database session to each request,
# and automatically closes it afterward -- even if an error occurs.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
