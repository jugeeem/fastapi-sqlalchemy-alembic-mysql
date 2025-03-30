# !/usr/bin/python
# -*- coding: utf-8 -*-
"""基本モデル定義モジュール

このモジュールでは、SQLAlchemyを使用したデータベースモデルの基底クラスを定義します。
全てのモデルがこの基本クラスを継承することで、共通フィールドや機能を持つようになります。
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import CHAR, TINYINT

from app.infrastructure.database import Base


class BaseModel(Base):
    """データベースモデルの基底クラス

    全てのデータベースモデルの基底となる抽象クラスです。
    共通のフィールド（ID、作成日時、更新日時など）とその動作を定義します。
    このクラスを直接インスタンス化することはできません。

    Attributes:
        id (str): モデルの一意識別子。UUIDv4形式で自動生成されます。
        remarks (str): 任意の備考。最大255文字、Null許容。
        created_at (datetime): レコードの作成日時。自動的に現在時刻が設定されます。
        created_by (str): レコードを作成したユーザーまたはシステムの識別子。
        updated_at (datetime): レコード最終更新日時。更新時に自動的に現在時刻に更新されます。
        updated_by (str): レコードを最後に更新したユーザーまたはシステムの識別子。
        delete_flag (int): 論理削除フラグ。0=有効、1=削除済み。
    """

    __abstract__ = True

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    remarks = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    created_by = Column(String(255), nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    updated_by = Column(String(255), nullable=False)
    delete_flag = Column(TINYINT(1), default=0, nullable=False)
