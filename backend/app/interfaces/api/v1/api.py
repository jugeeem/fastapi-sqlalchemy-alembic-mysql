from fastapi import APIRouter

from app.interfaces.api.v1.endpoints import attendances, auth, initialize, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    attendances.router, prefix="/attendances", tags=["attendances"]
)
api_router.include_router(initialize.router, prefix="/initialize", tags=["initialize"])
