# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザーモデル定義モジュール

このモジュールでは、ユーザーの認証情報を管理するためのデータベースモデルを定義します。
ユーザー名、メールアドレス、パスワードなどの基本的なユーザー認証情報を格納し、
プロフィール情報や連絡先情報、ロールとのリレーションシップを管理します。
"""

from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.models.base_model import BaseModel

# 型チェック時のみインポート
if TYPE_CHECKING:
    from app.infrastructure.models.user_contact import UserContactModel
    from app.infrastructure.models.user_profile import UserProfileModel
    from app.infrastructure.models.user_role import UserRoleModel


class UserModel(BaseModel):
    """ユーザー認証情報を管理するテーブル

    システム内のユーザーアカウントの主要な情報を格納するモデルです。
    認証に必要な基本情報（ユーザー名、メールアドレス、ハッシュ化されたパスワード）を保持し、
    ユーザープロフィール、連絡先情報、ロールへの参照を管理します。

    Attributes:
        username (str): ユーザーのログイン名。一意であり、インデックス付き。
        email (str): ユーザーのメールアドレス。インデックス付き。
        hashed_password (str): ハッシュ化されたパスワード。平文のパスワードは保存しません。
        profile (relationship): ユーザープロフィール情報へのリレーションシップ。1対1の関係。
        contact (relationship): ユーザー連絡先情報へのリレーションシップ。1対1の関係。
        roles (relationship): ユーザーに割り当てられたロールへのリレーションシップ。
                            UserRoleModelを介した多対多の関係。
    """

    __tablename__ = "users"

    # 認証情報
    username: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # リレーションシップ
    profile: Mapped["UserProfileModel"] = relationship(
        back_populates="user", uselist=False
    )
    contact: Mapped["UserContactModel"] = relationship(
        back_populates="user", uselist=False
    )
    roles: Mapped[List["UserRoleModel"]] = relationship(back_populates="user")
