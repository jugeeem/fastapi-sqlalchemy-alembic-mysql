# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザーエンティティモジュール

このモジュールでは、システム内のユーザーを表現するためのエンティティを定義します。
ユーザーはシステムの中心的なドメインオブジェクトであり、認証情報、個人情報、連絡先情報、
および権限情報を持ちます。
"""

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from app.domain.value_objects.enums import Gender


class User:
    """ユーザーエンティティクラス

    システム内のユーザーを表現するエンティティです。
    このクラスは、ユーザーの認証情報（ユーザー名、メール、パスワード）、個人情報（名前、性別、生年月日）、
    連絡先情報（電話番号、郵便番号、住所）、およびロール情報を含みます。

    Attributes:
        id (UUID, optional): ユーザーの一意識別子。
        username (str): ユーザーのログイン名。
        email (str): ユーザーのメールアドレス。
        hashed_password (str): ハッシュ化されたパスワード。
        first_name (str, optional): ユーザーの名（ファーストネーム）。
        first_name_ruby (str, optional): 名のフリガナ。
        last_name (str, optional): ユーザーの姓（ラストネーム）。
        last_name_ruby (str, optional): 姓のフリガナ。
        gender (Gender, optional): ユーザーの性別。
        birth_day (date, optional): ユーザーの生年月日。
        phone_number (str, optional): ユーザーの電話番号。
        zip_code (str, optional): ユーザーの郵便番号。
        address (str, optional): ユーザーの住所。
        role_ids (List[UUID], optional): ユーザーに割り当てられたロールIDのリスト。
        created_at (datetime, optional): 作成日時。
        created_by (str, optional): 作成者。
        updated_at (datetime, optional): 更新日時。
        updated_by (str, optional): 更新者。
        delete_flag (int, optional): 論理削除フラグ。0=有効、1=削除済み。
    """

    def __init__(
        self,
        id: Optional[UUID] = None,
        username: str = None,
        email: str = None,
        hashed_password: str = None,
        first_name: Optional[str] = None,
        first_name_ruby: Optional[str] = None,
        last_name: Optional[str] = None,
        last_name_ruby: Optional[str] = None,
        gender: Optional[Gender] = None,
        birth_day: Optional[date] = None,
        phone_number: Optional[str] = None,
        zip_code: Optional[str] = None,
        address: Optional[str] = None,
        role_ids: Optional[List[UUID]] = None,
        created_at: Optional[datetime] = None,
        created_by: Optional[str] = None,
        updated_at: Optional[datetime] = None,
        updated_by: Optional[str] = None,
        delete_flag: Optional[int] = 0,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.first_name = first_name
        self.first_name_ruby = first_name_ruby
        self.last_name = last_name
        self.last_name_ruby = last_name_ruby
        self.gender = gender
        self.birth_day = birth_day
        self.phone_number = phone_number
        self.zip_code = zip_code
        self.address = address
        self.role_ids = role_ids
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.delete_flag = delete_flag
