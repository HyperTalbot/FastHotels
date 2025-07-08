from fastapi import APIRouter

from .hotels.hotels_views import router as hotels_router
from .users.users_views import router as users_router
from .owners.owners_views import router as owners_router
from .reviews.reviews_views import router as reviews_router
from .rooms.rooms_views import router as rooms_router


router = APIRouter()
router.include_router(router=hotels_router, prefix="/hotels")
router.include_router(router=users_router, prefix="/users")
router.include_router(router=owners_router, prefix="/owners")
router.include_router(router=reviews_router, prefix="/reviews")
router.include_router(router=rooms_router, prefix="/rooms")
