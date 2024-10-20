from datetime import date

from DBBTestTask.contrib.library.models import (
    Author,
    AuthorBase,
    Book,
    BookBase,
    BookBorrowBase,
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
    in_stock: bool | None = True


class BookUpdate(BookBase):
    name: str | None = None
    ISBN: str | None = None
    publish_date: date | None = None
    genre_id: int | None = None
    publisher_id: int | None = None
    author_id: int | None = None


class BookRead(BookBase):
    id: int
    in_stock: bool
    name: str | None = None
    ISBN: str | None = None
    publish_date: date | None = None
    genre: Genre | None = None
    publisher: Publisher | None = None
    author: Author | None = None

class BookBorrowCreate(BookBorrowBase):
    date_borrowed: date
    date_to_return: date
    date_returned: date | None = None
    book_id: int
    user_id: int


class BookBorrowRead(BookBorrowCreate):
    pass
