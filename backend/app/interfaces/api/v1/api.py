from fastapi import APIRouter

from app.interfaces.api.v1.endpoints import users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
