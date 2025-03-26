from fastapi import APIRouter

from app.interfaces.api.v1.endpoints import attendances, users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    attendances.router, prefix="/attendances", tags=["attendances"]
)
