from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Message(BaseModel):
    message: str
    
class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
    first_name: Optional[str] = None  # Add this line
    last_name: Optional[str] = None    # Add this line


    class Config:
        from_attributes = True  # Updated from orm_mode

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Updated from orm_mode