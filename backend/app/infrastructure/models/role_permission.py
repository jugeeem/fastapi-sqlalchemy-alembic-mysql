# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ロール権限関連モデル定義モジュール

このモジュールでは、ロールと権限の多対多の関連を管理するための中間テーブルモデルを定義します。
ロールに複数の権限を割り当て、権限を複数のロールに関連付けるための構造を提供します。
"""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.models.base_model import BaseModel

# 型チェック時のみインポート
if TYPE_CHECKING:
    from app.infrastructure.models.permission import PermissionModel
    from app.infrastructure.models.role import RoleModel


class RolePermissionModel(BaseModel):
    """ロールと権限の関連を管理する中間テーブル

    ロールと権限の間の多対多の関係を実現するための中間（ジャンクション）テーブルです。
    各レコードは、特定のロールに特定の権限が割り当てられていることを表します。
    このテーブルにより、ロールに複数の権限を割り当て、各権限を複数のロールに関連付けることができます。

    Attributes:
        role_id (UUID): ロールの一意識別子。rolesテーブルの外部キー。
        permission_id (UUID): 権限の一意識別子。permissionsテーブルの外部キー。
        role (relationship): 関連するロールモデルへのリレーションシップ。
        permission (relationship): 関連する権限モデルへのリレーションシップ。
    """

    __tablename__ = "role_permissions"

    role_id: Mapped[UUID] = mapped_column(
        CHAR(36), ForeignKey("roles.id"), nullable=False
    )
    permission_id: Mapped[UUID] = mapped_column(
        CHAR(36), ForeignKey("permissions.id"), nullable=False
    )

    # リレーションシップ
    role: Mapped["RoleModel"] = relationship(back_populates="permissions")
    permission: Mapped["PermissionModel"] = relationship(
        back_populates="roles"
    )
