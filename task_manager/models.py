from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String(255), unique=True, index=True, nullable=False)  # Added length 255
    hashed_password = Column(String(255), nullable=False)                         # Added length 255
    created_at      = Column(DateTime, server_default=func.now())
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(255), index=True)                                  # Added length 255
    description = Column(String(255), nullable=True)                              # Added length 255
    completed   = Column(Boolean, default=False)
    owner_id    = Column(Integer, ForeignKey("users.id"), index=True)
    created_at  = Column(DateTime, server_default=func.now())
    updated_at  = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="tasks")