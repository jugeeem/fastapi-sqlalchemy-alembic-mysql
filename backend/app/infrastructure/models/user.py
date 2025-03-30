# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザーモデル定義モジュール

このモジュールでは、ユーザーの認証情報を管理するためのデータベースモデルを定義します。
ユーザー名、メールアドレス、パスワードなどの基本的なユーザー認証情報を格納し、
プロフィール情報や連絡先情報、ロールとのリレーションシップを管理します。
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.infrastructure.models.base_model import BaseModel


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
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # リレーションシップ
    profile = relationship(
        "UserProfileModel", back_populates="user", uselist=False
    )
    contact = relationship(
        "UserContactModel", back_populates="user", uselist=False
    )
    roles = relationship("UserRoleModel", back_populates="user")
