# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザーエンドポイントモジュール

このモジュールでは、ユーザー関連のAPIエンドポイントを定義します。
ユーザーの作成、取得、更新、削除などの操作を提供します。
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.dtos.user_dto import UserCreateDTO, UserResponseDTO
from app.application.services.user_service import UserService
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database import get_db
from app.infrastructure.repositories.user_repository import (
    SQLAlchemyUserRepository,
)

router = APIRouter()


def get_user_repository(
    db: Annotated[Session, Depends(get_db)],
) -> UserRepository:
    """ユーザーリポジトリのインスタンスを取得する

    データベースセッションを使用してSQLAlchemyユーザーリポジトリを初期化します。
    FastAPIの依存性注入システムで使用するための関数です。

    Args:
        db(Session): SQLAlchemyのデータベースセッション

    Returns:
        UserRepository: 初期化されたユーザーリポジトリインスタンス
    """
    return SQLAlchemyUserRepository(db)


def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    """ユーザーサービスのインスタンスを取得する

    ユーザーリポジトリを使用してユーザーサービスを初期化します。
    FastAPIの依存性注入システムで使用するための関数です。

    Args:
        repo(UserRepository): ユーザーリポジトリのインスタンス

    Returns:
        UserService: 初期化されたユーザーサービスインスタンス
    """
    return UserService(repo)


@router.post(
    "/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED
)
def create_user(
    user_create: UserCreateDTO,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """新規ユーザーを作成する

    ユーザー作成DTOを受け取り、新しいユーザーをデータベースに登録します。
    作成されたユーザーの情報をレスポンスとして返します。

    Args:
        user_create(UserCreateDTO): ユーザー作成に必要な情報を含むDTO.
        user_service(UserService): ユーザー関連の操作を行うサービス.

    Returns:
        UserResponseDTO: 作成されたユーザーの情報.

    Raises:
        HTTPException: ユーザー作成時にエラーが発生した場合（400 Bad Request）.
    """
    try:
        return user_service.create_user(user_create)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
