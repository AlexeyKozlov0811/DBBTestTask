from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from db import get_session
from DBBTestTask.contrib.library.models import Book
from DBBTestTask.contrib.library.serializers import BookCreate, BookRead, BookUpdate
from DBBTestTask.contrib.users.auth import get_current_user

router = APIRouter(prefix='/books', tags=['books'])

@router.get('', response_model=list[BookRead])
async def get_books_list(offset: int = 0, limit: int = Query(default=100, lte=100),
                         session: Session = Depends(get_session)):
    return Book.read_objects(offset=offset, limit=limit, session=session)

@router.get('/{book_id}', response_model=BookRead)
async def get_book(book_id: int, session: Session = Depends(get_session)):
    return Book.read_object(obj_id=book_id, session=session)

@router.post('', response_model=BookRead)
async def create_book(book: BookCreate, session: Session = Depends(get_session)):
    return Book.create_obj(data=book, session=session)

@router.patch('/{book_id}', response_model=BookRead)
async def update_book(book_id: int, book_data: BookUpdate, session: Session = Depends(get_session)):
    return Book.update_obj(obj_id=book_id, data=book_data, session=session)

@router.delete("/{book_id}")
async def delete_book(book_id: int, session: Session = Depends(get_session)):
    return Book.delete_obj(obj_id=book_id, session=session)

@router.get('/{book_id}/borrow')
async def borrow_book(book_id: int, session: Session = Depends(get_session),
                      current_user: str = Depends(get_current_user)):
    book = Book.get_obj_or_404(obj_id=book_id, session=session)
    return book
