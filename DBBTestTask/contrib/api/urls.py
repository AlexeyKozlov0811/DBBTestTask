from fastapi import APIRouter

from DBBTestTask.contrib.library.api import views as library_views
from DBBTestTask.contrib.users.api import views as users_views

router = APIRouter(prefix='/api')

router.include_router(library_views.router)
router.include_router(users_views.router)
