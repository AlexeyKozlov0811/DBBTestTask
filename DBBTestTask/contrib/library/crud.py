"""
    Table param represents DB Table class
    Other SQLModel typed params are data schemas
"""

from fastapi import Depends, HTTPException
from sqlmodel import Session, SQLModel, select
from starlette import status

from db import get_session


class ModelCRUD:
    @classmethod
    def create_obj(cls: type(SQLModel), data: SQLModel, session: Session = Depends(get_session)):
        data_to_db = cls.model_validate(data)
        session.add(data_to_db)
        session.commit()
        session.refresh(data_to_db)
        return data_to_db

    @classmethod
    def get_obj_or_404(cls: type(SQLModel), obj_id: int, session: Session = Depends(get_session)):
        obj = session.get(cls, obj_id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object not found with id: {obj_id}",
            )
        return obj

    @classmethod
    def read_objects(cls: type(SQLModel), offset: int = 0, limit: int = 20, session: Session = Depends(get_session)):
        list_of_objects = session.exec(select(cls).offset(offset).limit(limit)).all()
        return list_of_objects

    @classmethod
    def update_obj(cls: type(SQLModel), obj_id: int, data: SQLModel, session: Session = Depends(get_session)):
        obj_to_update = cls.get_obj_or_404(obj_id, cls, session)

        obj_data = data.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(obj_to_update, key, value)

        session.add(obj_to_update)
        session.commit()
        session.refresh(obj_to_update)
        return obj_to_update

    @classmethod
    def delete_obj(cls: type(SQLModel), obj_id: int, session: Session = Depends(get_session)):
        obj = cls.get_obj_or_404(obj_id, cls, session)

        session.delete(obj)
        session.commit()
        return {"ok": True}
