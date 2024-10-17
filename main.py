from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel
from starlette.responses import RedirectResponse

from Library.api.urls import register_routes

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# Initialize SQLite DB
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Call the function to register routes
register_routes(app)

@app.get("/")
async def root():
    return RedirectResponse(url="docs")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
