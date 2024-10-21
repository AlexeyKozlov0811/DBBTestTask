from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from db import get_session
from DBBTestTask.contrib.library.models import Publisher
from DBBTestTask.contrib.library.serializers import PublisherCreate, PublisherRead, PublisherUpdate

router = APIRouter(prefix="/publishers", tags=["publishers"])


@router.get("", response_model=list[PublisherRead])
async def get_publishers_list(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: Session = Depends(get_session),
):
    return Publisher.read_objects(offset=offset, limit=limit, session=session)


@router.get("/{publisher_id}", response_model=PublisherRead)
async def get_publisher(publisher_id: int, session: Session = Depends(get_session)):
    return Publisher.get_obj_or_404(obj_id=publisher_id, session=session)


@router.post("", response_model=PublisherRead)
async def create_publisher(publisher: PublisherCreate, session: Session = Depends(get_session)):
    return Publisher.create_obj(data=publisher, session=session)


@router.patch("/{publisher_id}", response_model=PublisherRead)
async def update_publisher(
    publisher_id: int, publisher_data: PublisherUpdate, session: Session = Depends(get_session)
):
    return Publisher.update_obj(obj_id=publisher_id, data=publisher_data, session=session)


@router.delete("/{publisher_id}")
async def delete_publisher(publisher_id: int, session: Session = Depends(get_session)):
    return Publisher.delete_obj(obj_id=publisher_id, session=session)
