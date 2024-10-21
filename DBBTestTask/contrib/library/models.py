from datetime import date

from sqlmodel import Field, Relationship, SQLModel

from DBBTestTask.contrib.library.crud import ModelCRUD
from DBBTestTask.contrib.library.validators import (
    AuthorValidators,
    BookValidators,
    PublisherValidators,
)


# Authors models
class AuthorBase(SQLModel, AuthorValidators):
    name: str = Field(index=True, unique=True)
    birth_date: date = Field()


class Author(AuthorBase, ModelCRUD, table=True):
    id: int | None = Field(default=None, primary_key=True)
    books: list["Book"] = Relationship(back_populates="author")


# Genre models
class GenreBase(SQLModel):
    name: str = Field(index=True, unique=True)


class Genre(GenreBase, ModelCRUD, table=True):
    id: int | None = Field(default=None, primary_key=True)

    books: list["Book"] = Relationship(back_populates="genre")


# Publishers models
class PublisherBase(SQLModel, PublisherValidators):
    name: str = Field(index=True, unique=True)
    est_date: date = Field()


class Publisher(PublisherBase, ModelCRUD, table=True):
    id: int | None = Field(default=None, primary_key=True)
    books: list["Book"] = Relationship(back_populates="publisher")


# Books models
class BookBase(SQLModel, BookValidators):
    name: str = Field(index=True, unique=True)
    ISBN: str = Field(index=True, unique=True)
    publish_date: date = Field()

    genre_id: int = Field(foreign_key="genre.id")
    publisher_id: int = Field(foreign_key="publisher.id")
    author_id: int = Field(foreign_key="author.id")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "test book",
                "ISBN": "1-111-11111-1",
                "publish_date": "2024-10-18",
                "genre_id": 1,
                "publisher_id": 1,
                "author_id": 1,
            }
        }


class Book(BookBase, ModelCRUD, table=True):
    id: int | None = Field(default=None, primary_key=True)
    in_stock: bool = Field(default=True)
    genre: Genre = Relationship(back_populates="books")
    publisher: Publisher = Relationship(back_populates="books")
    author: Author = Relationship(back_populates="books")
    borrowings: list["BookBorrow"] = Relationship(back_populates="book", cascade_delete=True)

    @classmethod
    def get_sort_fields(cls):
        return {"name", "ISBN", "publish_date"}

    @classmethod
    def get_sort_related_field(cls):
        """sort config format {<field_alias>: (<Model>, <Model field>)}"""
        return {
            "author_name": (Author, Author.name),
            "genre_name": (Genre, Genre.name),
            "publisher_name": (Publisher, Publisher.name),
        }


class BookBorrowBase(SQLModel):
    date_borrowed: date = Field()
    date_to_return: date = Field()
    date_returned: date | None = Field()
    book_id: int = Field(foreign_key="book.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)


class BookBorrow(BookBorrowBase, ModelCRUD, table=True):
    book: "Book" = Relationship(back_populates="borrowings")
    user: "User" = Relationship(back_populates="borrowings")

    @property
    def is_overdue(self) -> bool:
        return date.today() > self.date_to_return and self.date_returned in None

    @property
    def is_returned(self) -> bool:
        return self.date_returned is not None
