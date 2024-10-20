from datetime import datetime

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel

from DBBTestTask.contrib.library.models import BookBorrow


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    # TODO: enforce validation
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str = Field(min_length=60, max_length=128)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    borrowings: list['BookBorrow'] = Relationship(back_populates="user")


# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str
    email: str | None

class UserData(BaseModel):
    id: int | None
    username: str
    email: str | None
    is_active: bool

    class Config:
        from_attributes = True

class UserInDB(UserCreate):
    hashed_password: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
