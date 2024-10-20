from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, or_
from starlette.status import HTTP_201_CREATED

from db import get_session
from DBBTestTask.contrib.users.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from DBBTestTask.contrib.users.models import Token, User, UserCreate, UserData

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
):
    # TODO: Fix deprecated queries
    db_user = session.query(User).filter(User.username == form_data.username).first()
    if db_user is None or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create the access token
    access_token = create_access_token(data={"sub": db_user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register/", status_code=HTTP_201_CREATED)
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = (
        session.query(User)
        .filter(or_(User.username == user.username, User.email == user.email))
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")

    # Create a new user
    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
        email=user.email,
    )

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error in saving user")

    return {"user_id": new_user.id}


@router.get("/me", response_model=UserData)
async def read_current_user(current_user: UserData = Depends(get_current_user)):
    return UserData.model_validate(current_user)
