from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from db import create_db_and_tables
from DBBTestTask.contrib.api.urls import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Register routs
app.include_router(api_router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="docs")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
