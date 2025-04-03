# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
ユーザー作成エンドポイントモジュール。

このモジュールは、FastAPI を使用して新しいユーザーを作成するエンドポイントを提供します。
ユーザー作成に必要な情報を受け取り、データベースに登録する機能を実装しています。

エンドポイント:
    - POST /: 新しいユーザーを作成します。
"""

from fastapi import APIRouter, HTTPException, status

from app.application.dtos.user_dto import UserCreateDTO, UserResponseDTO
from app.dependency.users import UserDependency

router = APIRouter()


@router.post(
    "/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED
)
def create_user(
    user_create: UserCreateDTO,
    user_service: UserDependency,
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
