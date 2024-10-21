"""
Table param represents DB Table class
Other SQLModel typed params are data schemas
"""

from fastapi import Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, SQLModel, select
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from db import get_session


class ModelCRUD:
    @classmethod
    def create_obj(cls: type(SQLModel), data: SQLModel, session: Session = Depends(get_session)):
        try:
            data_to_db = cls.model_validate(data)
            session.add(data_to_db)
            session.commit()
            session.refresh(data_to_db)
            return data_to_db
        except SQLAlchemyError as e:
            # TODO: would be good to sanitize error message
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

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
    def read_objects(
        cls: type(SQLModel),
        offset: int = 0,
        limit: int = 20,
        sort_by: str | None = None,
        sort_order: str = 'asc',
        session: Session = Depends(get_session),
    ):
        statement = select(cls).offset(offset).limit(limit)
        if sort_by is not None:
            related_sortable_fields = set(cls.get_sort_related_field().keys())
            sortable_fields =  related_sortable_fields | cls.get_sort_fields()

            if sort_by not in sortable_fields:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid sort field")

            if sort_by in related_sortable_fields:
                sort_config = cls.get_sort_related_field()[sort_by]
                sort_column = sort_config[1]
                statement = statement.join(sort_config[0])
            else:
                sort_column = getattr(cls, sort_by)
            if sort_order == "desc":
                sort_column = sort_column.desc()

            statement = statement.order_by(sort_column)

        list_of_objects = session.exec(statement).all()
        return list_of_objects

    @classmethod
    def update_obj(
        cls: type(SQLModel), obj_id: int, data: SQLModel, session: Session = Depends(get_session)
    ):
        try:
            obj_to_update = cls.get_obj_or_404(obj_id, session)

            obj_data = data.model_dump(exclude_unset=True)
            for key, value in obj_data.items():
                setattr(obj_to_update, key, value)

            session.add(obj_to_update)
            session.commit()
            session.refresh(obj_to_update)
            return obj_to_update
        except SQLAlchemyError as e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

    @classmethod
    def delete_obj(cls: type(SQLModel), obj_id: int, session: Session = Depends(get_session)):
        obj = cls.get_obj_or_404(obj_id, session)

        session.delete(obj)
        session.commit()
        return {"ok": True}
