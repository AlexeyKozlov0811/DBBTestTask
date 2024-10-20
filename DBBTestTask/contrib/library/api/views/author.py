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
from DBBTestTask.contrib.library.models import Author, AuthorCreate, AuthorRead, AuthorUpdate

router = APIRouter(prefix='/authors', tags=['authors'])

@router.get('', response_model=list[AuthorRead])
async def get_authors_list(offset: int = 0, limit: int = Query(default=100, lte=100),
                         session: Session = Depends(get_session)):
    return read_objects(table=Author, offset=offset, limit=limit, session=session)

@router.get('/{author_id}', response_model=AuthorRead)
async def get_author(author_id: int, session: Session = Depends(get_session)):
    return read_object(obj_id=author_id, table=Author, session=session)

@router.post('', response_model=AuthorRead)
async def create_author(author: AuthorCreate, session: Session = Depends(get_session)):
    return create_obj(data=author, table=Author, session=session)

@router.patch('/{author_id}', response_model=AuthorRead)
async def update_author(author_id: int, author_data: AuthorUpdate, session: Session = Depends(get_session)):
    return update_obj(obj_id=author_id, data=author_data, table=Author, session=session)

@router.delete("/{author_id}")
async def delete_author(author_id: int, session: Session = Depends(get_session)):
    return delete_obj(obj_id=author_id, table=Author, session=session)
