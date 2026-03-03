# Importing SQLAlchemy tools for database connection and ORM setup
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
#using these to acess environment variables securely
import os
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

#connecting the URL to get database connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create database engine (manages connections to PostgreSQL)
engine = create_engine(DATABASE_URL)


# Create session factory (used to create new DB sessions per request)
SessionLocal = sessionmaker(bind=engine)


# Base class for all SQLAlchemy models
Base = declarative_base()


# Dependency function for FastAPI
# This creates a new DB session for each request
def get_db():
    db = SessionLocal()   #Open new session
    try:
        yield db          #Provide session to endpoint
    finally:
        db.close()        #always close session after request ends