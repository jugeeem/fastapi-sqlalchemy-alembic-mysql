# !/usr/bin/python
# -*- coding: utf-8 -*-
"""データベースモデルの基底モジュール。

このモジュールはSQLAlchemyを使用したデータベースモデルの基底クラスを提供します。
アプリケーション全体で使用される共通の属性とメソッドを定義し、
一貫したデータベース操作とデータ整合性を確保します。
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, text
from sqlalchemy.dialects.mysql import CHAR, TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class BaseModel(Base):
    """データベースモデルの基底クラス。

    全てのデータベースモデルの基底となる抽象クラスです。
    共通のフィールド（ID、作成日時、更新日時など）とその動作を定義します。
    このクラスを直接インスタンス化することはできません。

    Attributes:
        id: モデルの一意識別子。UUIDv4形式で自動生成されます。
        remarks: 任意の備考。最大255文字、Null許容。
        created_at: レコードの作成日時。自動的に現在時刻が設定されます。
        created_by: レコードを作成したユーザーまたはシステムの識別子。
        updated_at: レコード最終更新日時。更新時に自動的に現在時刻に更新されます。
        updated_by: レコードを最後に更新したユーザーまたはシステムの識別子。
        delete_flag: 論理削除フラグ。0=有効、1=削除済み。
    """

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        CHAR(36), primary_key=True, default=lambda: str(uuid4())
    )
    remarks: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        nullable=False,
    )
    updated_by: Mapped[str] = mapped_column(String(255), nullable=False)
    delete_flag: Mapped[int] = mapped_column(
        TINYINT(1), default=0, nullable=False
    )
