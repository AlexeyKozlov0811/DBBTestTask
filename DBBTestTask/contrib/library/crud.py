"""
    Table param represents DB Table class
    Other SQLModel typed params are data schemas
"""

from fastapi import Depends, HTTPException
from sqlmodel import Session, SQLModel, select
from starlette import status

from db import get_session


def get_obj_or_404(obj_id: int, table: type(SQLModel), session: Session = Depends(get_session)):
    obj = session.get(table, obj_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Object not found with id: {obj_id}",
        )

def create_obj(data: SQLModel, table: type(SQLModel), session: Session = Depends(get_session)):
    data_to_db = table.model_validate(data)
    session.add(data_to_db)
    session.commit()
    session.refresh(data_to_db)
    return data_to_db


def read_objects(table: type(SQLModel), offset: int = 0, limit: int = 20, session: Session = Depends(get_session)):
    list_of_objects = session.exec(select(table).offset(offset).limit(limit)).all()
    return list_of_objects


def read_object(obj_id: int, table: type(SQLModel), session: Session = Depends(get_session)):
    return get_obj_or_404(obj_id, table, session)


def update_obj(obj_id: int, data: SQLModel, table: type(SQLModel), session: Session = Depends(get_session)):
    obj_to_update = get_obj_or_404(obj_id, table, session)

    obj_data = data.model_dump(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(obj_to_update, key, value)

    session.add(obj_to_update)
    session.commit()
    session.refresh(obj_to_update)
    return obj_to_update


def delete_obj(obj_id: int, table: type(SQLModel), session: Session = Depends(get_session)):
    obj = get_obj_or_404(obj_id, table, session)

    session.delete(obj)
    session.commit()
    return {"ok": True}
