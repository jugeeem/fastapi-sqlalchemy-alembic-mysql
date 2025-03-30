# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ロールモデル定義モジュール

このモジュールでは、システム内のユーザーロールを管理するためのデータベースモデルを定義します。
ロールはユーザーに割り当てられる権限のグループであり、アクセス制御に使用されます。
"""

from sqlalchemy import Column, Enum, Text
from sqlalchemy.orm import relationship

from app.domain.value_objects.enums import Role
from app.infrastructure.models.base_model import BaseModel


class RoleModel(BaseModel):
    """ユーザーロールを管理するテーブル

    システム内のユーザーロール（権限グループ）を表現するモデルです。
    各ロールは名前と説明を持ち、複数のユーザーと複数の権限に関連付けることができます。
    アプリケーション内のアクセス制御の基本単位として機能します。

    Attributes:
        name (Role): ロールの名前。Roleという列挙型を使用。一意であり、インデックス付き。
        description (str): ロールの詳細な説明。
        users (relationship): このロールが割り当てられているユーザーとのリレーションシップ。
                            UserRoleModelを介した多対多の関係。
        permissions (relationship): このロールに割り当てられている権限とのリレーションシップ。
                                  RolePermissionModelを介した多対多の関係。
    """

    __tablename__ = "roles"

    name = Column(Enum(Role), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # リレーションシップ
    users = relationship("UserRoleModel", back_populates="role")
    permissions = relationship("RolePermissionModel", back_populates="role")
