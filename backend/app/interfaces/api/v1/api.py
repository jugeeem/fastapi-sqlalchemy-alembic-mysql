# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
APIルーター統合モジュール。

このモジュールは、バージョン1（v1）のAPIエンドポイントを統合するためのルーターを提供します。
各エンドポイントモジュールをインクルードし、API全体のルーティングを管理します。

エンドポイント:
    - /users: ユーザー関連のエンドポイントを提供します。
    - /initialize: 初期化関連のエンドポイントを提供します。
"""

from fastapi import APIRouter

from app.interfaces.api.v1.endpoints.initialize import (
    router as initialize_router,
)
from app.interfaces.api.v1.endpoints.users.api import router as users_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(
    initialize_router, prefix="/initialize", tags=["initialize"]
)
