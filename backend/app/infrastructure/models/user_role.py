# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザーロール関連モデル定義モジュール

このモジュールでは、ユーザーとロールの多対多の関連を管理するための中間テーブルモデルを定義します。
ユーザーに複数のロールを割り当て、ロールに複数のユーザーを所属させるための構造を提供します。
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

from app.infrastructure.models.base_model import BaseModel


class UserRoleModel(BaseModel):
    """ユーザーとロールの関連を管理する中間テーブル

    ユーザーとロールの間の多対多の関係を実現するための中間（ジャンクション）テーブルです。
    各レコードは、特定のユーザーに特定のロールが割り当てられていることを表します。
    このテーブルにより、ユーザーに複数のロールを割り当て、各ロールに複数のユーザーを所属させることができます。

    Attributes:
        user_id (str): ユーザーの一意識別子。usersテーブルの外部キー。
        role_id (str): ロールの一意識別子。rolesテーブルの外部キー。
        user (relationship): 関連するユーザーモデルへのリレーションシップ。
        role (relationship): 関連するロールモデルへのリレーションシップ。
    """

    __tablename__ = "user_roles"

    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    role_id = Column(CHAR(36), ForeignKey("roles.id"), nullable=False)

    # リレーションシップ
    user = relationship("UserModel", back_populates="roles")
    role = relationship("RoleModel", back_populates="users")
