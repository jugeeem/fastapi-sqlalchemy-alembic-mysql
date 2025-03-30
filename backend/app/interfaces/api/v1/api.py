from fastapi import APIRouter

from app.interfaces.api.v1.endpoints.initialize import (
    router as initialize_router,
)
from app.interfaces.api.v1.endpoints.users import router as users_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(
    initialize_router, prefix="/initialize", tags=["initialize"]
)
