# !/usr/bin/python
# -*- coding: utf-8 -*-
"""権限モデル定義モジュール

このモジュールでは、システム内の権限を管理するためのデータベースモデルを定義します。
権限は特定の機能や操作へのアクセスを制御するために使用されます。
"""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.models.base_model import BaseModel

# 型チェック時のみインポート
if TYPE_CHECKING:
    from app.infrastructure.models.role_permission import RolePermissionModel


class PermissionModel(BaseModel):
    """権限を管理するテーブル

    システム内の個別の権限（アクセス許可）を表現するモデルです。
    各権限は名前と説明を持ち、ロールに割り当てることができます。
    ユーザーは割り当てられたロールを通じて間接的に権限を持ちます。

    Attributes:
        name (str): 権限の名前。一意であり、最大255文字。インデックス付き。
        description (str): 権限の詳細な説明。
        roles (relationship): この権限が割り当てられているロールとのリレーションシップ。
                             RolePermissionModelを介した多対多の関係。
    """

    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # リレーションシップ
    roles: Mapped[List["RolePermissionModel"]] = relationship(
        back_populates="permission"
    )
