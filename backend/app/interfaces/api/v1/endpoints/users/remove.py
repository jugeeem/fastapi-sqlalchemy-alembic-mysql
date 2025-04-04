# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザー情報削除APIエンドポイントモジュール

このモジュールでは、ユーザーのアカウントを削除するためのエンドポイントを定義します。
ユーザーは自分のアカウントを削除することができ、
その際に関連するデータも削除されます。
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, status

from app.dependency.users import UserDependency

router = APIRouter()


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="ユーザーアカウントの削除",
    description="指定されたユーザーIDに対応するユーザーアカウントを削除します。",
)
async def delete_user(
    user_id: Annotated[
        UUID,
        Path(
            title="ユーザーID",
            description="削除対象のユーザーの一意識別子",
        ),
    ],
    user_service: UserDependency,
) -> None:
    """ユーザーアカウント削除エンドポイント

    指定されたユーザーIDに対応するユーザーアカウントを削除します。
    削除後は204 No Contentレスポンスが返されます。

    Args:
        user_id (UUID): 削除対象のユーザーID
        user_service (UserService): ユーザーサービスインスタンス

    Raises:
        HTTPException: ユーザーが見つからない場合や削除に失敗した場合
    """
    try:
        user_service.remove_user(
            user_id=user_id, updated_by="system"
        )  # TODO: 認証機能を実装した際に変更予定
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    return None
