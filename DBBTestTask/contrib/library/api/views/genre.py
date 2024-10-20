from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from db import get_session
from DBBTestTask.contrib.library.models import Genre
from DBBTestTask.contrib.library.serializers import GenreCreate, GenreRead, GenreUpdate

router = APIRouter(prefix='/genres', tags=['genres'])

@router.get('', response_model=list[GenreRead])
async def get_genres_list(offset: int = 0, limit: int = Query(default=100, lte=100),
                         session: Session = Depends(get_session)):
    return Genre.read_objects(offset=offset, limit=limit, session=session)

@router.get('/{genre_id}', response_model=GenreRead)
async def get_genre(genre_id: int, session: Session = Depends(get_session)):
    return Genre.read_object(obj_id=genre_id, session=session)

@router.post('', response_model=GenreRead)
async def create_genre(genre: GenreCreate, session: Session = Depends(get_session)):
    return Genre.create_obj(data=genre, session=session)

@router.patch('/{genre_id}', response_model=GenreRead)
async def update_genre(genre_id: int, genre_data: GenreUpdate, session: Session = Depends(get_session)):
    return Genre.update_obj(obj_id=genre_id, data=genre_data, session=session)

@router.delete("/{genre_id}")
async def delete_genre(genre_id: int, session: Session = Depends(get_session)):
    return Genre.delete_obj(obj_id=genre_id, session=session)
