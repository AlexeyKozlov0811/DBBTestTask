from datetime import date

from sqlmodel import Field, Relationship, SQLModel

from DBBTestTask.contrib.library.validators import BookValidators


# Authors models
class AuthorBase(SQLModel):
    name: str = Field(index=True, unique=True)
    birth_date: date = Field()

class Author(AuthorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    books: list['Book'] = Relationship(back_populates="author")

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    name: str | None = None
    birth_date: date | None = None
    books: list['Book'] | None = None


class AuthorRead(AuthorUpdate):
    id: int

# Genre models
class GenreBase(SQLModel):
    name: str = Field(index=True, unique=True)

class Genre(GenreBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    books: list['Book'] = Relationship(back_populates="genre")

class GenreCreate(GenreBase):
    pass

class GenreUpdate(GenreBase):
    name: str | None = None
    books: list['Book'] | None = None

class GenreRead(GenreUpdate):
    id: int

# Publishers models
class PublisherBase(SQLModel):
    name: str = Field(index=True, unique=True)
    est_date: date = Field()

class Publisher(PublisherBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    books: list['Book'] = Relationship(back_populates="publisher")

class PublisherCreate(PublisherBase):
    pass

class PublisherUpdate(PublisherBase):
    name: str | None = None
    books: list['Book'] | None = None

class PublisherRead(PublisherUpdate):
    id: int

# Books models
class BookBase(SQLModel, BookValidators):
    name: str = Field(index=True, unique=True)
    ISBN: str = Field(index=True, unique=True)
    publish_date: date = Field()

    genre_id: int | None = Field(default=None, foreign_key="genre.id")
    publisher_id: int | None = Field(default=None, foreign_key="publisher.id")
    author_id: int | None = Field(default=None, foreign_key="author.id")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "test book",
                "ISBN": "1-111-11111-1",
                "publish_date": "2024-10-18",
                "genre_id": 0,
                "publisher_id": 0,
                "author_id": 0
            }
        }


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    genre: Genre = Relationship(back_populates="books")
    publisher: Publisher = Relationship(back_populates="books")
    author: Author = Relationship(back_populates="books")


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    name: str | None = None
    ISBN: str | None = None
    publish_date: date | None = None
    genre_id: int | None = None
    publisher_id: int | None = None
    author_id: int | None = None


class BookRead(BookUpdate):
    id: int
    genre: Genre | None = None
    publisher: Publisher | None = None
    author: Author | None = None
