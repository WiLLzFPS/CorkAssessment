# imports
import datetime
from sqlite3 import IntegrityError
from typing import Literal
from enum import Enum as PyEnum
from sqlalchemy import Enum as SAEnum, ForeignKey, create_engine, Column, Integer, String, DateTime, UniqueConstraint, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, Field

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

    # backref from Event
    events = relationship("Event", back_populates="user")

# model for login status
class LoginStatus(str, PyEnum):
    success = "success"
    failure = "failure"

# events table for multi-tenancy
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # FK connect to users table
    origin = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    idempotency_key = Column(String, nullable=False)
    status = Column(SAEnum(LoginStatus), nullable=False)

    # make sure all combinations of tenant_id and idempotency_key are unique
    __table_args__ = (
        UniqueConstraint("tenant_id", "idempotency_key", name="uq_tenant_idempotency"),
    )

    # backref from User
    user = relationship("User", back_populates="events")

# create a pydantic model for the event
class EventCreate(BaseModel):
    tenant_id: str = Field(...) # ... means required
    user_id: int = Field(...)
    origin: str = Field(...)
    timestamp: datetime.datetime
    idempotency_key: str
    status: Literal["success", "failure"]

class EventRead(EventCreate):
    id: int

# create a model for event response
class SuspiciousItem(BaseModel):
    origin: str
    count: int

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

# TODO: Write GET OPERATION: The GET request should return failed login origins that meet certain thresholds (N failed logins in the last X
#                            minutes for a tenant). The GET request should support pagination and should be sortable.