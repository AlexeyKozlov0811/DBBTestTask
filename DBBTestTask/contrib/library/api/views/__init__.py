from fastapi import APIRouter

from DBBTestTask.contrib.library.api.views import author, book, genre, publisher

router = APIRouter(prefix="/library")

router.include_router(book.router)
router.include_router(author.router)
router.include_router(genre.router)
router.include_router(publisher.router)
