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
from DBBTestTask.contrib.library.models import Genre, GenreCreate, GenreRead, GenreUpdate

router = APIRouter(prefix='/genres', tags=['genres'])

@router.get('', response_model=list[GenreRead])
async def get_genres_list(offset: int = 0, limit: int = Query(default=100, lte=100),
                         session: Session = Depends(get_session)):
    return read_objects(table=Genre, offset=offset, limit=limit, session=session)

@router.get('/{genre_id}', response_model=GenreRead)
async def get_genre(genre_id: int, session: Session = Depends(get_session)):
    return read_object(obj_id=genre_id, table=Genre, session=session)

@router.post('', response_model=GenreRead)
async def create_genre(genre: GenreCreate, session: Session = Depends(get_session)):
    return create_obj(data=genre, table=Genre, session=session)

@router.patch('/{genre_id}', response_model=GenreRead)
async def update_genre(genre_id: int, genre_data: GenreUpdate, session: Session = Depends(get_session)):
    return update_obj(obj_id=genre_id, data=genre_data, table=Genre, session=session)

@router.delete("/{genre_id}")
async def delete_genre(genre_id: int, session: Session = Depends(get_session)):
    return delete_obj(obj_id=genre_id, table=Genre, session=session)
