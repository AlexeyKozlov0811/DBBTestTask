from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from starlette import status

from db import get_session
from DBBTestTask import settings
from DBBTestTask.contrib.library.models import Book, BookBorrow
from DBBTestTask.contrib.library.serializers import (
    BookBorrowCreate,
    BookBorrowRead,
    BookCreate,
    BookRead,
    BookUpdate,
)
from DBBTestTask.contrib.users.auth import get_current_user
from DBBTestTask.contrib.users.models import UserData

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=list[BookRead])
async def get_books_list(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: Session = Depends(get_session),
):
    return Book.read_objects(offset=offset, limit=limit, session=session)


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, session: Session = Depends(get_session)):
    return Book.read_object(obj_id=book_id, session=session)


@router.post("", response_model=BookRead)
async def create_book(book: BookCreate, session: Session = Depends(get_session)):
    return Book.create_obj(data=book, session=session)


@router.patch("/{book_id}", response_model=BookRead)
async def update_book(book_id: int, book_data: BookUpdate, session: Session = Depends(get_session)):
    return Book.update_obj(obj_id=book_id, data=book_data, session=session)


@router.delete("/{book_id}")
async def delete_book(book_id: int, session: Session = Depends(get_session)):
    return Book.delete_obj(obj_id=book_id, session=session)


@router.post("/{book_id}/borrow", response_model=BookBorrowRead)
async def borrow_book(
    book_id: int,
    session: Session = Depends(get_session),
    current_user: UserData = Depends(get_current_user),
):
    book = Book.get_obj_or_404(obj_id=book_id, session=session)
    if book.in_stock:
        borrow_record = BookBorrow.create_obj(
            data=BookBorrowCreate(
                book_id=book.id,
                user_id=current_user.id,
                date_borrowed=date.today(),
                date_to_return=date.today() + timedelta(days=settings.BORROWING_DAYS),
            ),
            session=session,
        )

        book.in_stock = False
        session.add(book)
        session.commit()
        session.refresh(book)

        return borrow_record
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Book {book.name} is not available for borrowing",
    )


@router.post("/{book_id}/return", response_model=BookBorrowRead)
async def return_book(
    book_id: int,
    session: Session = Depends(get_session),
    current_user: UserData = Depends(get_current_user),
):
    book = Book.get_obj_or_404(obj_id=book_id, session=session)
    user_active_borrow = list(
        filter(
            lambda record: not record.is_returned and record.user_id == current_user.id,
            book.borrowings,
        )
    )
    if any(user_active_borrow):
        borrow_record = user_active_borrow[0]

        borrow_record.date_returned = date.today()
        book.in_stock = True
        session.add(borrow_record)
        session.add(book)
        session.commit()
        session.refresh(borrow_record)
        return borrow_record
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"You dont have an active borrow for the Book {book.name}",
    )


@router.get("/{book_id}/borrowing-history", response_model=list[BookBorrowRead])
async def get_borrow_history(book_id: int, session: Session = Depends(get_session)):
    book = Book.get_obj_or_404(obj_id=book_id, session=session)
    if any(book.borrowings):
        return book.borrowings
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Book {book.name} doesn't have any borrowing history",
    )
