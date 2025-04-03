# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
ユーザーエンドポイント統合モジュール。

このモジュールは、ユーザー関連のエンドポイントを統合するためのルーターを提供します。
ユーザー作成および取得のエンドポイントを含みます。

エンドポイント:
    - POST /: 新しいユーザーを作成します。
    - GET /{user_id}: ユーザーIDに基づいてユーザー情報を取得します。
"""

from fastapi import APIRouter

from app.interfaces.api.v1.endpoints.users.create import (
    router as create_router,
)
from app.interfaces.api.v1.endpoints.users.get import router as get_router
from app.interfaces.api.v1.endpoints.users.get_list import (
    router as get_list_router,
)

router = APIRouter()
router.include_router(create_router)
router.include_router(get_router)
router.include_router(get_list_router)
