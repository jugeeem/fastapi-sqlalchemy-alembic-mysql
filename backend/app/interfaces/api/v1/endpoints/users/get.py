# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
ユーザー取得エンドポイントモジュール。

このモジュールは、FastAPI を使用してユーザー情報を取得するエンドポイントを提供します。
指定されたユーザーIDに基づいて、ユーザー情報を取得する機能を実装しています。

エンドポイント:
    - GET /{user_id}: ユーザーIDに基づいてユーザー情報を取得します。
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.application.dtos.user_dto import UserCreateDTO, UserResponseDTO
from app.dependency.users import UserDependency

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponseDTO)
def get_user(
    user_id: UUID,
    user_service: UserDependency,
):
    """ユーザーIDでユーザーを取得する。

    指定されたユーザーIDに一致するユーザーの情報を返します。

    Args:
        user_id (UUID): 取得するユーザーのID。
        user_service (UserDependency): ユーザー関連の操作を行うサービス。

    Returns:
        UserResponseDTO: 取得したユーザーの情報。

    Raises:
        HTTPException: 指定されたIDのユーザーが見つからない場合に発生します。
            - 404 Not Found: 指定されたIDのユーザーが見つからない場合。
    """
    try:
        return user_service.get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
