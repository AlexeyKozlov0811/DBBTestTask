from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from db import get_session
from DBBTestTask.contrib.library.crud import (
    create_obj,
    delete_obj,
    read_object,
    read_objects,
    update_obj,
)
from DBBTestTask.contrib.library.models import Book, BookCreate, BookRead, BookUpdate

router = APIRouter(prefix='/books', tags=['books'])

@router.get('', response_model=list[BookRead])
async def get_books_list(offset: int = 0, limit: int = Query(default=100, lte=100),
                         session: Session = Depends(get_session)):
    return read_objects(table=Book, offset=offset, limit=limit, session=session)

@router.get('/{book_id}', response_model=BookRead)
async def get_book(book_id: int, session: Session = Depends(get_session)):
    return read_object(obj_id=book_id, table=Book, session=session)

@router.post('', response_model=BookRead)
async def create_book(book: BookCreate, session: Session = Depends(get_session)):
    return create_obj(data=book, table=Book, session=session)

@router.patch('/{book_id}', response_model=BookRead)
async def update_book(book_id: int, book_data: BookUpdate, session: Session = Depends(get_session)):
    return update_obj(obj_id=book_id, data=book_data, table=Book, session=session)

@router.delete("/{book_id}")
async def delete_book(book_id: int, session: Session = Depends(get_session)):
    return delete_obj(obj_id=book_id, table=Book, session=session)
