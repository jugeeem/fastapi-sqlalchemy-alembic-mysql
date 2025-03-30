# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザー連絡先モデル定義モジュール

このモジュールでは、ユーザーの連絡先情報を管理するためのデータベースモデルを定義します。
電話番号、郵便番号、住所などの連絡先情報を格納し、ユーザーモデルとの関連を管理します。
また、電話番号や郵便番号の形式を検証するための制約も定義しています。
"""

from sqlalchemy import CheckConstraint, Column, ForeignKey, String
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

from app.infrastructure.models.base_model import BaseModel


class UserContactModel(BaseModel):
    """ユーザーの連絡先情報を管理するテーブル

    システム内のユーザーの連絡先情報を格納するモデルです。
    ユーザー認証情報とは別に、電話番号、郵便番号、住所などの連絡先情報を管理します。
    usersテーブルと1対1の関係を持ちます。
    電話番号と郵便番号については、特定の形式に従っていることを保証する制約が設定されています。

    Attributes:
        user_id (str): 関連するユーザーの一意識別子。usersテーブルの外部キー。
        phone_number (str): ユーザーの電話番号。形式は「000-0000-0000」、Null許容。
        zip_code (str): ユーザーの郵便番号。形式は「000-0000」、Null許容。
        address (str): ユーザーの住所。最大255文字、Null許容。
        user (relationship): 関連するユーザーモデルへのリレーションシップ。1対1の関係。

    Constraints:
        check_phone_format: 電話番号が000-0000-0000の形式に従うことを検証する制約。
        check_zipcode_format: 郵便番号が000-0000の形式に従うことを検証する制約。
    """

    __tablename__ = "user_contacts"

    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    phone_number = Column(String(13), nullable=True)
    zip_code = Column(String(8), nullable=True)
    address = Column(String(255), nullable=True)

    # リレーションシップ
    user = relationship("UserModel", back_populates="contact")

    # 制約
    __table_args__ = (
        CheckConstraint(
            "phone_number IS NULL OR phone_number REGEXP '^[0-9]{3}-[0-9]{4}-[0-9]{4}$'",
            name="check_phone_format",
        ),
        CheckConstraint(
            "zip_code IS NULL OR zip_code REGEXP '^[0-9]{3}-[0-9]{4}$'",
            name="check_zipcode_format",
        ),
    )
