from fastapi import APIRouter

from DBBTestTask.contrib.library.api.views import book

router = APIRouter(prefix='/library')

router.include_router(book.router)
