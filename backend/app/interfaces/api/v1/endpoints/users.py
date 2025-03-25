from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError, OperationalError

from app.application.dtos.user_dto import UserCreateDTO, UserUpdateDTO, UserResponseDTO
from app.application.services.user_service import UserService
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database import get_db
from app.infrastructure.repositories.user_repository import SQLAlchemyUserRepository

router = APIRouter()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return SQLAlchemyUserRepository(db)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)


@router.get("", response_model=List[UserResponseDTO])
def read_users(
    service: UserService = Depends(get_user_service),
):
    return service.get_users()


@router.post("", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreateDTO,
    service: UserService = Depends(get_user_service),
):
    try:
        return service.create_user(user_create)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except (ProgrammingError, OperationalError) as e:
        if "Table" in str(e) and "doesn't exist" in str(e):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="データベーステーブルが存在しません。マイグレーションを実行してください: `alembic upgrade head`",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"データベースエラー: {str(e)}",
        )


@router.get("/{user_id}", response_model=UserResponseDTO)
def read_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
):
    try:
        user = service.get_user(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{user_id}", response_model=UserResponseDTO)
def update_user(
    user_id: str,
    user_update: UserUpdateDTO,
    service: UserService = Depends(get_user_service),
):
    try:
        user = service.update_user(user_id, user_update)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
):
    try:
        if not service.delete_user(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
