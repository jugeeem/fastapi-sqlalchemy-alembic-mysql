# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザー関連の依存性（依存性注入）を提供するモジュール。

このモジュールはFastAPIの依存性注入システムで使用される関数と型を定義します。
ユーザーリポジトリとユーザーサービスの取得方法を提供します。
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services.user_service import UserService
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database import get_db
from app.infrastructure.repositories.user_repository import (
    SQLAlchemyUserRepository,
)


def get_user_repository(
    db: Annotated[Session, Depends(get_db)],
) -> UserRepository:
    """ユーザーリポジトリのインスタンスを取得する

    データベースセッションを使用してSQLAlchemyユーザーリポジトリを初期化します。
    FastAPIの依存性注入システムで使用するための関数です。

    Args:
        db(Session): SQLAlchemyのデータベースセッション

    Returns:
        UserRepository: 初期化されたユーザーリポジトリインスタンス
    """

    return SQLAlchemyUserRepository(db)


def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    """ユーザーサービスのインスタンスを取得する

    ユーザーリポジトリを使用してユーザーサービスを初期化します。
    FastAPIの依存性注入システムで使用するための関数です。

    Args:
        repo(UserRepository): ユーザーリポジトリのインスタンス

    Returns:
        UserService: 初期化されたユーザーサービスインスタンス
    """

    return UserService(repo)


UserDependency = Annotated[UserService, Depends(get_user_service)]
"""ユーザーサービスをFastAPIのエンドポイントに注入するための型アノテーション。

この型は、FastAPIのエンドポイント関数の引数に使用することで、
自動的にユーザーサービスのインスタンスが注入されるようにします。

例:
    ```python
    @app.get("/users/")
    def get_users(user_service: UserDependency):
        return user_service.get_all_users()
    ```
"""
