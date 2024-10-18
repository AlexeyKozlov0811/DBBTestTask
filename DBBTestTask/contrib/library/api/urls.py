from fastapi import FastAPI

from DBBTestTask.contrib.library.api import views


def register_routes(app: FastAPI):
    app.include_router(views.router, prefix="/api")
