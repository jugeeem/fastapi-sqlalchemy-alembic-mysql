# !/usr/bin/python
# -*- coding: utf-8 -*-
"""データベース接続モジュール

このモジュールでは、SQLAlchemyを使用したデータベース接続の設定と管理を行います。
データベースセッションの作成、管理、およびFastAPI依存性注入システム用のセッション提供関数を定義します。
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    scoped_session,
    sessionmaker,
)

from app.config import settings

# データベースエンジンの初期化
engine = create_engine(settings.DATABASE_URL, pool_recycle=3600)
# セッションファクトリの作成（スレッドセーフなスコープ付きセッション）
SessionLocal = scoped_session(sessionmaker(autoflush=False, bind=engine))


# SQLAlchemyモデル定義の基底クラス
class Base(DeclarativeBase):
    """SQLAlchemyモデルの基底クラス"""

    pass


def init_db() -> None:
    """データベース初期化関数

    この関数はデータベースの初期化処理を行います。
    現在はAlembicによるマイグレーション管理を使用しているため、実際には使用されていません。
    開発時の便宜的な用途として残されています。

    Returns:
        None
    """
    # Alembicを使用してマイグレーションを行うため、ここでのテーブル作成は不要
    # 開発時のみの便宜的なものとして残すことも可能
    pass


def get_db() -> Generator[Session, None, None]:
    """データベースセッションを提供する関数

    FastAPIの依存性注入システムで使用されるジェネレータ関数です。
    エンドポイント関数内でデータベースセッションを使用するために、
    この関数を依存関係として注入します。
    セッションはリクエスト処理後に自動的にクローズされます。

    Yields:
        Session: SQLAlchemyデータベースセッション

    Example:
        ```python
        @router.get("/items")
        def read_items(db: Annotated[Session, Depends(get_db)]):
            return db.query(Item).all()
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
