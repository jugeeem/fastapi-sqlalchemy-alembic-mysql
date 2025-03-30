# !/usr/bin/python
# -*- coding: utf-8 -*-
"""権限モデル定義モジュール

このモジュールでは、システム内の権限を管理するためのデータベースモデルを定義します。
権限は特定の機能や操作へのアクセスを制御するために使用されます。
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.infrastructure.models.base_model import BaseModel


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

    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # リレーションシップ
    roles = relationship("RolePermissionModel", back_populates="permission")
