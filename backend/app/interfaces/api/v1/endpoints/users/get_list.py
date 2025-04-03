# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザー一覧取得エンドポイント

このモジュールでは、ユーザー一覧を取得するAPIエンドポイントを定義します。
クエリパラメータによるページネーションとソート機能をサポートしています。
"""

from typing import Annotated

from fastapi import APIRouter, Query, status

from app.application.dtos.user_dto import UserGetListQueryDTO, UserResponseDTO
from app.dependency.users import UserDependency

router = APIRouter()


@router.get(
    "/", response_model=list[UserResponseDTO], status_code=status.HTTP_200_OK
)
async def get_users(
    user_service: UserDependency,
    query: Annotated[UserGetListQueryDTO, Query()],
):
    """ユーザー一覧を取得する

    ページネーションとソート順に対応したユーザー一覧を取得します。

    Args:
        user_service (UserService): ユーザーサービス（依存性注入）
        query (UserGetListQueryDTO): クエリパラメータを含むDTO

    Returns:
        List[UserResponseDTO]: ユーザー情報のリスト
    """

    is_ascending = True if query.ascending == "true" else False

    return user_service.get_users(
        offset=query.offset, limit=query.limit, ascending=is_ascending
    )
