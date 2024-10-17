from fastapi import FastAPI

from Library.api import views


def register_routes(app: FastAPI):
    app.include_router(views.router, prefix="/api")
