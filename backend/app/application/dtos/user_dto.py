# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザーDTOモジュール

このモジュールでは、ユーザー関連のデータ転送オブジェクト（DTO）を定義します。
DTOはAPIとドメイン層の間でデータを受け渡すための構造体として機能し、
入力バリデーションとレスポンス形式の定義を行います。
"""

import re
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.domain.value_objects.enums import Gender


class UserCreateDTO(BaseModel):
    """ユーザー作成リクエスト用DTO

    APIからユーザー作成リクエストを受け取るためのDTOです。
    クライアントから送信されたデータのバリデーションを行い、
    ユーザー作成に必要な情報を構造化された形式で提供します。

    Attributes:
        username (str): ユーザーのログイン名。3～50文字の長さ。
        email (EmailStr): 有効なメールアドレス。
        password (str): パスワード。最低8文字の長さ。
        first_name (str, optional): ユーザーの名（ファーストネーム）。
        first_name_ruby (str, optional): 名のフリガナ。
        last_name (str, optional): ユーザーの姓（ラストネーム）。
        last_name_ruby (str, optional): 姓のフリガナ。
        gender (Gender): ユーザーの性別。Genderという列挙型を使用。
        birth_day (date): ユーザーの生年月日。
        phone_number (str, optional): ユーザーの電話番号。形式は「000-0000-0000」。
        zip_code (str, optional): ユーザーの郵便番号。形式は「000-0000」。
        address (str, optional): ユーザーの住所。
    """

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    first_name_ruby: Optional[str] = None
    last_name: Optional[str] = None
    last_name_ruby: Optional[str] = None
    gender: Gender
    birth_day: date
    phone_number: Optional[str] = None
    zip_code: Optional[str] = None
    address: Optional[str] = None

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        """電話番号のフォーマットを検証する

        電話番号が000-0000-0000の形式に従っているかを検証します。

        Args:
            v (str): 検証する電話番号

        Returns:
            str: 検証済みの電話番号

        Raises:
            ValueError: 電話番号の形式が不正な場合
        """
        if v and not re.match(r"^[0-9]{3}-[0-9]{4}-[0-9]{4}$", v):
            raise ValueError("Phone number must be in format: 000-0000-0000")
        return v

    @field_validator("zip_code")
    def validate_zip_code(cls, v):
        """郵便番号のフォーマットを検証する

        郵便番号が000-0000の形式に従っているかを検証します。

        Args:
            v (str): 検証する郵便番号

        Returns:
            str: 検証済みの郵便番号

        Raises:
            ValueError: 郵便番号の形式が不正な場合
        """
        if v and not re.match(r"^[0-9]{3}-[0-9]{4}$", v):
            raise ValueError("Zip code must be in format: 000-0000")
        return v


class UserResponseDTO(BaseModel):
    """ユーザー情報レスポンス用DTO

    APIからユーザー情報を返すためのDTOです。
    ドメインエンティティからAPIレスポンス形式へのデータ変換を行い、
    クライアントに必要な情報を提供します。パスワード等の機密情報は除外されます。

    Attributes:
        id (UUID): ユーザーの一意識別子。
        username (str): ユーザーのログイン名。
        email (str): ユーザーのメールアドレス。
        first_name (str, optional): ユーザーの名（ファーストネーム）。
        first_name_ruby (str, optional): 名のフリガナ。
        last_name (str, optional): ユーザーの姓（ラストネーム）。
        last_name_ruby (str, optional): 姓のフリガナ。
        gender (Gender): ユーザーの性別。
        birth_day (date): ユーザーの生年月日。
        phone_number (str, optional): ユーザーの電話番号。
        zip_code (str, optional): ユーザーの郵便番号。
        address (str, optional): ユーザーの住所。
        role_ids (List[UUID]): ユーザーに割り当てられたロールIDのリスト。
        created_at (datetime): 作成日時。
        created_by (str): 作成者。
        updated_at (datetime): 更新日時。
        updated_by (str): 更新者。
        delete_flag (int): 論理削除フラグ。0=有効、1=削除済み。
    """

    id: UUID
    username: str
    email: str
    first_name: Optional[str]
    first_name_ruby: Optional[str]
    last_name: Optional[str]
    last_name_ruby: Optional[str]
    gender: Gender
    birth_day: date
    phone_number: Optional[str]
    zip_code: Optional[str]
    address: Optional[str]
    role_ids: List[UUID]
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    delete_flag: int

    model_config = ConfigDict(from_attributes=True)
