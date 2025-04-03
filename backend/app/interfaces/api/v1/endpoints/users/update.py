# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザー情報更新APIエンドポイントモジュール

このモジュールでは、ユーザーの個人情報と連絡先情報を更新するためのエンドポイントを定義します。
ユーザープロフィール情報（名前、性別、生年月日など）と連絡先情報（電話番号、郵便番号、住所）の
更新を処理します。
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, status

from app.application.dtos.user_dto import UserResponseDTO, UserUpdateDTO
from app.dependency.users import UserDependency

router = APIRouter()


@router.put(
    "/{user_id}",
    response_model=UserResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="ユーザー情報の更新",
    description="指定されたユーザーIDに対応するユーザーの個人情報と連絡先情報を更新します。",
)
async def update_user(
    user_id: Annotated[
        UUID,
        Path(
            title="ユーザーID",
            description="更新対象のユーザーの一意識別子",
        ),
    ],
    user_data: UserUpdateDTO,
    user_service: UserDependency,
) -> UserResponseDTO:
    """ユーザー情報更新エンドポイント

    指定されたユーザーIDに対応するユーザーの個人情報と連絡先情報を更新します。
    更新対象は、ユーザープロフィール（名前、性別、生年月日など）と
    連絡先情報（電話番号、郵便番号、住所）です。

    Args:
        user_id (UUID): 更新対象のユーザーID
        user_data (UserUpdateDTO): 更新するユーザー情報データ
        user_service (UserService): ユーザーサービスインスタンス

    Returns:
        UserResponseDTO: 更新されたユーザー情報

    Raises:
        HTTPException: ユーザーが見つからない場合や更新に失敗した場合
    """
    try:
        updated_user = user_service.update_user(
            user_id=user_id,
            user_dto=user_data,
            updated_by="system",  # TODO: 認証機能を実装した際に変更予定
        )
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user information",
        ) from e
