# !/usr/bin/python
# -*- coding: utf-8 -*-
"""初期ロール作成エンドポイントモジュール

このモジュールでは、システムで使用する初期ロールを作成するためのAPIエンドポイントを定義します。
ロールは、ユーザーのアクセス権限を管理するための重要な要素です。
このエンドポイントを使用して、ADMIN、MANAGER、USER、GUESTの標準ロールをデータベースに登録します。
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.domain.value_objects.enums import Role
from app.infrastructure.database import get_db
from app.infrastructure.models.role import RoleModel

router = APIRouter()


@router.post(
    "/roles",
    status_code=status.HTTP_201_CREATED,
)
def create_roles(
    db: Annotated[Session, Depends(get_db)],
):
    """初期ロールを作成する

    システムで使用する基本的なロールを作成します。ADMIN、MANAGER、USER、GUESTの
    標準ロールをデータベースに登録します。

    Args:
        db(Session): SQLAlchemyのデータベースセッション

    Returns:
        dict: 作成成功メッセージを含む辞書
            {"message": "Roles created successfully."}

    Raises:
        SQLAlchemyError: データベース操作に失敗した場合
    """

    roles = [
        RoleModel(
            name=Role.ADMIN.value,
            description="Administrator",
            created_by="system",
            updated_by="system",
        ),
        RoleModel(
            name=Role.MANAGER.value,
            description="Manager",
            created_by="system",
            updated_by="system",
        ),
        RoleModel(
            name=Role.USER.value,
            description="Regular User",
            created_by="system",
            updated_by="system",
        ),
        RoleModel(
            name=Role.GUEST.value,
            description="Guest User",
            created_by="system",
            updated_by="system",
        ),
    ]

    db.add_all(roles)
    db.commit()
    return {"message": "Roles created successfully."}
