# imports
from sqlite3 import IntegrityError
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum, UniqueConstraint, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

from fastapi import FastAPI, Depends, HTTPException

# create api instance
app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

# create engine to connect to database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# create session to interact with database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for declarative models
Base = declarative_base()

# create a user model class
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# create the database tables
Base.metadata.create_all(bind=engine)

# create a model for the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


# POST OPERATION: create a user within the database
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = User(name=user.name, email=user.email)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already registered")
    return user