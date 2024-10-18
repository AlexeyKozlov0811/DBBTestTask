import re
from datetime import date

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class Books(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    ISBN: str = Field(index=True, unique=True)
    publish_date: date = Field()

    @field_validator('publish_date')
    def validate_publish_date(cls, value):
        if value > date.today():
            raise ValueError("Publish date can't be in the future")
        return value

    @field_validator('ISBN')
    def validate_publish_date(cls, value):
        if value > date.today():
            raise ValueError("Publish date can't be in the future")
        return value

    @field_validator('ISBN')
    def validate_isbn(cls, value):
        if not (cls.is_valid_isbn10(value) or cls.is_valid_isbn13(value)):
            raise ValueError('Invalid ISBN format. Must be a valid ISBN-10 or ISBN-13.')
        return value

    @staticmethod
    def is_valid_isbn10(isbn: str) -> bool:
        # Match pattern with dashes: X-XXX-XXXXX-X
        if not re.match(r'^\d{1}-\d{3}-\d{5}-[\dX]$', isbn):
            return False
        # Remove dashes and validate checksum
        isbn = isbn.replace("-", "")
        total = sum((i + 1) * (10 if x == 'X' else int(x)) for i, x in enumerate(isbn))
        return total % 11 == 0

    @staticmethod
    def is_valid_isbn13(isbn: str) -> bool:
        # Match pattern with dashes: XXX-X-XX-XXXXX-X
        if not re.match(r'^\d{3}-\d{1}-\d{2}-\d{5}-\d{1}$', isbn):
            return False
        # Remove dashes and validate checksum
        isbn = isbn.replace("-", "")
        total = sum((1 if i % 2 == 0 else 3) * int(x) for i, x in enumerate(isbn))
        return total % 10 == 0


class Authors(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
