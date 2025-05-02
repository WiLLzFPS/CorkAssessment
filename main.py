# imports
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from fastapi import FastAPI

# create api instance
app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

# create engine to connect to database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# create session to interact with database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for declarative models
Base = declarative_base()

