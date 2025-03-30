# !/usr/bin/python
# -*- coding: utf-8 -*-
"""設定モジュール

このモジュールでは、アプリケーションの設定を管理します。
設定は環境変数から読み込まれ、アプリケーション全体で使用されます。
設定の変更は、環境変数を変更することで行います。
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定クラス

    アプリケーション全体の設定を管理するためのクラスです。
    Pydanticを使用して環境変数から設定値を取得し、型変換とバリデーションを行います。

    Attributes:
        PROJECT_NAME (str): プロジェクト名。デフォルトは"FastAPI DDD Example"。
        API_V1_STR (str): APIバージョン1のURLプレフィックス。デフォルトは"/api/v1"。
        DATABASE_URL (str): データベース接続URL。必須項目。
        SECURITY_KEY (str): セキュリティキー。JWT署名などに使用。必須項目。
        ALGORITHM (str): 暗号化アルゴリズム。JWT署名などに使用。必須項目。
        ACCESS_TOKEN_EXPIRE_MINUTES (int): アクセストークンの有効期限（分）。必須項目。
    """

    # General settings
    PROJECT_NAME: str = "FastAPI DDD Example"
    API_V1_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL: str

    # Security settings
    SECURITY_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


# グローバルに使用可能な設定インスタンス
settings = Settings()
