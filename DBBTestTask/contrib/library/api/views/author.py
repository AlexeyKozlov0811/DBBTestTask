from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from db import get_session
from DBBTestTask.contrib.library.models import Author
from DBBTestTask.contrib.library.serializers import AuthorCreate, AuthorRead, AuthorUpdate

router = APIRouter(prefix='/authors', tags=['authors'])

"""
    4. GET /authors/{id}/books: • List all books written by a specific author.
    I haven't created separate endpoint for this since this data can be retrieved via regular read endpoints
"""

@router.get('', response_model=list[AuthorRead])
async def get_authors_list(offset: int = 0, limit: int = Query(default=100, lte=100),
                         session: Session = Depends(get_session)):
    return Author.read_objects(offset=offset, limit=limit, session=session)

@router.get('/{author_id}', response_model=AuthorRead)
async def get_author(author_id: int, session: Session = Depends(get_session)):
    return Author.read_object(obj_id=author_id, session=session)

@router.post('', response_model=AuthorRead)
async def create_author(author: AuthorCreate, session: Session = Depends(get_session)):
    return Author.create_obj(data=author, session=session)

@router.patch('/{author_id}', response_model=AuthorRead)
async def update_author(author_id: int, author_data: AuthorUpdate, session: Session = Depends(get_session)):
    return Author.update_obj(obj_id=author_id, data=author_data, session=session)

@router.delete("/{author_id}")
async def delete_author(author_id: int, session: Session = Depends(get_session)):
    return Author.delete_obj(obj_id=author_id, session=session)
