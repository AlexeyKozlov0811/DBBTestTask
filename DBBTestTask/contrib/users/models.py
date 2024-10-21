from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from DBBTestTask.contrib.library.models import BookBorrow
from DBBTestTask.contrib.library.serializers import BookBorrowRead


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: EmailStr = Field(index=True, unique=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(min_length=60, max_length=128)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    borrowings: list["BookBorrow"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int | None
    username: str
    email: str | None
    is_active: bool
    borrowings: list[BookBorrowRead]


class UserInDB(UserCreate):
    hashed_password: str


class UserLoginRequest(SQLModel):
    username: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str
