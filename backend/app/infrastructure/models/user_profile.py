# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザープロフィールモデル定義モジュール

このモジュールでは、ユーザーの個人プロフィール情報を管理するためのデータベースモデルを定義します。
名前、フリガナ、性別、生年月日などの個人情報を格納し、ユーザーモデルとの関連を管理します。
"""

from datetime import date
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Date, Enum, ForeignKey, String
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.enums import Gender
from app.infrastructure.models.base_model import BaseModel

# 型チェック時のみインポート
if TYPE_CHECKING:
    from app.infrastructure.models.user import UserModel


class UserProfileModel(BaseModel):
    """ユーザーの個人プロフィール情報を管理するテーブル

    システム内のユーザーの個人プロフィール情報を格納するモデルです。
    ユーザー認証情報とは別に、表示名や個人属性などの情報を管理します。
    usersテーブルと1対1の関係を持ちます。

    Attributes:
        user_id (UUID): 関連するユーザーの一意識別子。usersテーブルの外部キー。
        first_name (str): ユーザーの名（ファーストネーム）。最大255文字、Null許容。
        first_name_ruby (str): 名のフリガナ。最大255文字、Null許容。
        last_name (str): ユーザーの姓（ラストネーム）。最大255文字、Null許容。
        last_name_ruby (str): 姓のフリガナ。最大255文字、Null許容。
        gender (Gender): ユーザーの性別。Genderという列挙型を使用。
        birth_day (Date): ユーザーの生年月日。
        user (relationship): 関連するユーザーモデルへのリレーションシップ。1対1の関係。
    """

    __tablename__ = "user_profiles"

    user_id: Mapped[UUID] = mapped_column(
        CHAR(36), ForeignKey("users.id"), nullable=False
    )
    first_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    first_name_ruby: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    last_name_ruby: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    birth_day: Mapped[date] = mapped_column(Date, nullable=False)

    # リレーションシップ
    user: Mapped["UserModel"] = relationship(back_populates="profile")
