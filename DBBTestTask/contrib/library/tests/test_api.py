# TODO: create hypothesis and schemathesis tests
from datetime import date, timedelta

import pytest
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from DBBTestTask import settings
from DBBTestTask.contrib.library.models import Author, Book, BookBorrow, Genre, Publisher
from DBBTestTask.contrib.library.serializers import (
    AuthorCreate,
    BookBorrowCreate,
    BookCreate,
    GenreCreate,
    PublisherCreate,
)


class TestBookBorrowAPI:
    @pytest.fixture()
    def books(self, session, user):
        genre = Genre.create_obj(data=GenreCreate(name='test_genre'), session=session)
        author = Author.create_obj(data=AuthorCreate(name='test_author', birth_date=date.today()), session=session)
        publisher = Publisher.create_obj(data=PublisherCreate(name='test_genre', est_date=date.today()), session=session)

        available_book = Book.create_obj(
            data=BookCreate(
                name='test_book', publish_date=date.today(), ISBN="1-111-11111-1",
                genre_id=genre.id, author_id=author.id, publisher_id=publisher.id
            ), session=session)

        unavailable_book = Book.create_obj(
            data=BookCreate(
                name='test_unavailable_book', publish_date=date.today(), ISBN="2-222-22222-2",
                genre_id=genre.id, author_id=author.id, publisher_id=publisher.id, in_stock=False
            ), session=session)

        BookBorrow.create_obj(
            data=BookBorrowCreate(
                date_borrowed=date.today(), date_to_return=date.today() + timedelta(days=1),
                book_id=unavailable_book.id, user_id=user.id
            ), session=session)

        books = {"available_books": [available_book], "borrowed_books": [unavailable_book]}
        return books

    @pytest.fixture()
    def auth_urls(self, books):
        return {
            'borrow_available': f'/api/library/books/{books['available_books'][0].id}/borrow',
            'borrow_unavailable': f'/api/library/books/{books['borrowed_books'][0].id}/borrow',
            'return_available': f'/api/library/books/{books['borrowed_books'][0].id}/return',
            'return_unavailable': f'/api/library/books/{books['available_books'][0].id}/return',
            'borrowing_history': f'/api/library/books/{books['borrowed_books'][0].id}/borrowing-history',
            'empty_borrowing_history': f'/api/library/books/{books['available_books'][0].id}/borrowing-history',
        }

    def test_borrow_book(self, session, books, auth_urls, client_logged, user):
        book_to_borrow = books['available_books'][0]
        assert book_to_borrow.in_stock is True
        resp = client_logged.post(auth_urls['borrow_available'])
        assert resp.status_code == HTTP_200_OK

        data = resp.json()
        assert data['book_id'] == book_to_borrow.id
        assert data['user_id'] == user.id
        assert data['date_borrowed'] == date.today().isoformat()
        assert data['date_to_return'] == (date.today() + timedelta(days=settings.BORROWING_DAYS)).isoformat()
        assert data['date_returned'] is None

    def test_borrow_book_unauthorized(self, session, books, auth_urls, client, user):
        resp = client.post(auth_urls['borrow_available'])
        assert resp.status_code == HTTP_401_UNAUTHORIZED

    def test_borrow_unavailable_book(self, session, books, auth_urls, client_logged, user):
        borrowed_book = books['borrowed_books'][0]
        assert borrowed_book.in_stock is False
        resp = client_logged.post(auth_urls['borrow_unavailable'])
        assert resp.status_code == HTTP_400_BAD_REQUEST

        data = resp.json()
        assert borrowed_book.in_stock is False
        assert borrowed_book.name in data['detail']

    def test_return_book(self, session, books, auth_urls, client_logged, user):
        borrowed_book = books['borrowed_books'][0]
        assert borrowed_book.in_stock is False
        resp = client_logged.post(auth_urls['return_available'])
        assert resp.status_code == HTTP_200_OK

        data = resp.json()
        assert borrowed_book.in_stock is True
        assert data['date_returned'] == date.today().isoformat()

    def test_return_invalid_book(self, session, books, auth_urls, client_logged, user):
        available_book = books['available_books'][0]
        assert available_book.in_stock is True
        resp = client_logged.post(auth_urls['return_unavailable'])
        assert resp.status_code == HTTP_400_BAD_REQUEST

        data = resp.json()
        assert available_book.in_stock is True
        assert available_book.name in data['detail']

    def test_borrowing_history(self, session, books, auth_urls, client_logged):
        available_book = books['borrowed_books'][0]
        assert available_book.in_stock is False
        resp = client_logged.get(auth_urls['borrowing_history'])
        assert resp.status_code == HTTP_200_OK

    def test_empty_borrowing_history(self, session, books, auth_urls, client_logged):
        available_book = books['available_books'][0]
        assert available_book.in_stock is True
        resp = client_logged.get(auth_urls['empty_borrowing_history'])
        assert resp.status_code == HTTP_400_BAD_REQUEST
        data = resp.json()
        assert available_book.name in data['detail']

