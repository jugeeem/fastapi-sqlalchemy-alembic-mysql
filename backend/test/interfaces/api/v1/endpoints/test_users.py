# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザーエンドポイントテストモジュール

このモジュールでは、ユーザー関連のAPIエンドポイントに対するテストケースを定義します。
ユーザー作成エンドポイントの正常系・異常系テストなどを含みます。
"""

import uuid

from fastapi import status
from fastapi.testclient import TestClient

from app.config import settings


class TestCreateUser:
    """ユーザー作成エンドポイントのテストケース

    ユーザー作成エンドポイント（POST /api/v1/users/）に対する
    様々なテストケースを定義します。
    """

    def test_create_user_success(self, client: TestClient, valid_user_data):
        """有効なデータでユーザーが正常に作成できることを確認

        正常なユーザーデータを使用して、ユーザーが正常に作成されることをテストします。

        Args:
            client (TestClient): FastAPIのテストクライアント
            valid_user_data (dict): 有効なユーザーデータ
        """
        response = client.post(
            f"{settings.API_V1_STR}/users/", json=valid_user_data
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == valid_user_data["username"]
        assert data["email"] == valid_user_data["email"]
        assert "id" in data
        assert (
            "password" not in data
        )  # パスワードはレスポンスに含まれないことを確認

    def test_create_user_invalid_email(
        self, client: TestClient, valid_user_data
    ):
        """無効なメールアドレスでエラーが返されることを確認

        無効なメールアドレス形式を使用した場合に、
        適切なエラーレスポンスが返されることをテストします。

        Args:
            client (TestClient): FastAPIのテストクライアント
            valid_user_data (dict): 有効なユーザーデータ（一部変更して使用）
        """
        invalid_data = valid_user_data.copy()
        invalid_data["email"] = "invalid-email"

        response = client.post(
            f"{settings.API_V1_STR}/users/", json=invalid_data
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "detail" in data

    def test_create_user_short_password(
        self, client: TestClient, valid_user_data
    ):
        """短すぎるパスワードでエラーが返されることを確認

        最小文字数未満のパスワードを使用した場合に、
        適切なエラーレスポンスが返されることをテストします。

        Args:
            client (TestClient): FastAPIのテストクライアント
            valid_user_data (dict): 有効なユーザーデータ（一部変更して使用）
        """
        invalid_data = valid_user_data.copy()
        invalid_data["password"] = "short"

        response = client.post(
            f"{settings.API_V1_STR}/users/", json=invalid_data
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "detail" in data

    def test_create_user_invalid_phone_number(
        self, client: TestClient, valid_user_data
    ):
        """無効な電話番号形式でエラーが返されることを確認

        不正な形式の電話番号を使用した場合に、
        適切なエラーレスポンスが返されることをテストします。

        Args:
            client (TestClient): FastAPIのテストクライアント
            valid_user_data (dict): 有効なユーザーデータ（一部変更して使用）
        """
        invalid_data = valid_user_data.copy()
        invalid_data["phone_number"] = "12345678"  # 正しい形式ではない

        response = client.post(
            f"{settings.API_V1_STR}/users/", json=invalid_data
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "detail" in data

    def test_create_user_missing_required_field(
        self, client: TestClient, valid_user_data
    ):
        """必須フィールドが欠けている場合にエラーが返されることを確認

        必須フィールドを省略した場合に、
        適切なエラーレスポンスが返されることをテストします。

        Args:
            client (TestClient): FastAPIのテストクライアント
            valid_user_data (dict): 有効なユーザーデータ（一部変更して使用）
        """
        invalid_data = valid_user_data.copy()
        del invalid_data["username"]  # 必須フィールドを削除

        response = client.post(
            f"{settings.API_V1_STR}/users/", json=invalid_data
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "detail" in data


class TestGetUser:
    """ユーザー取得エンドポイントのテストケース

    ユーザー取得エンドポイント（GET /api/v1/users/{user_id}）に対する
    様々なテストケースを定義します。
    """

    def test_get_user_success(self, client: TestClient, valid_user_data):
        """存在するユーザーIDでユーザーが正常に取得できることを確認

        有効なユーザーIDを使用して、ユーザーが正常に取得されることをテストします。

        Args:
            client (TestClient): FastAPIのテストクライアント
            valid_user_data (dict): 有効なユーザーデータ
        """
        # 事前にユーザーを作成
        create_response = client.post(
            f"{settings.API_V1_STR}/users/", json=valid_user_data
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_user = create_response.json()
        user_id = created_user["id"]

        # ユーザーIDを使用してユーザーを取得
        response = client.get(f"{settings.API_V1_STR}/users/{user_id}")

        # 検証
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == valid_user_data["username"]
        assert data["email"] == valid_user_data["email"]
        assert (
            "password" not in data
        )  # パスワードはレスポンスに含まれないことを確認

    def test_get_user_not_found(self, client: TestClient):
        """存在しないユーザーIDで404エラーが返されることを確認

        存在しないユーザーIDを使用した場合に、
        適切なエラーレスポンスが返されることをテストします。

        Args:
            client (TestClient): FastAPIのテストクライアント
        """
        # 存在しないUUID
        non_existent_user_id = str(uuid.uuid4())

        # リクエスト
        response = client.get(
            f"{settings.API_V1_STR}/users/{non_existent_user_id}"
        )

        # 検証
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data
