from datetime import date

from DBBTestTask.contrib.library.models import (
    Author,
    AuthorBase,
    Book,
    BookBase,
    Genre,
    GenreBase,
    Publisher,
    PublisherBase,
)


class PublisherCreate(PublisherBase):
    pass


class PublisherUpdate(PublisherBase):
    name: str | None = None
    books: list[Book] | None = None


class PublisherRead(PublisherUpdate):
    id: int


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    name: str | None = None
    books: list[Book] | None = None


class GenreRead(GenreUpdate):
    id: int


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    name: str | None = None
    birth_date: date | None = None
    books: list[Book] | None = None


class AuthorRead(AuthorUpdate):
    id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    name: str | None = None
    ISBN: str | None = None
    publish_date: date | None = None
    genre_id: int | None = None
    publisher_id: int | None = None
    author_id: int | None = None


class BookRead(BookBase):
    id: int
    name: str | None = None
    ISBN: str | None = None
    publish_date: date | None = None
    genre: Genre | None = None
    publisher: Publisher | None = None
    author: Author | None = None
