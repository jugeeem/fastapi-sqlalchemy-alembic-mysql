import json
import uuid
from datetime import datetime
from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient

from app.infrastructure.models.user import UserModel
from app.infrastructure.models.user_info import UserInfoModel


def create_test_user_in_db(db_session):
    """テスト用のユーザーをデータベースに作成"""
    user_id = str(uuid.uuid4())
    db_user = UserModel(
        id=user_id,
        username="testuser",
        email="test@example.com",
        password="password123",
        manager_id=str(uuid.uuid4()),
        remarks="Test user",
        delete_flag=False,
        created_at=datetime.now(),
        created_by="test",
        updated_at=datetime.now(),
        updated_by="test",
    )
    db_session.add(db_user)

    user_info = UserInfoModel(
        id=str(uuid.uuid4()),
        user_id=user_id,
        first_name="Test",
        first_name_ruby="テスト",
        last_name="User",
        last_name_ruby="ユーザー",
        phone_number="123-456-7890",
        zip_code="123-4567",
        address="Tokyo, Japan",
        delete_flag=False,
        created_at=datetime.now(),
        created_by="test",
        updated_at=datetime.now(),
        updated_by="test",
    )
    db_session.add(user_info)
    db_session.commit()
    return user_id


class TestUsersAPI:
    def test_read_users_empty(self, client: TestClient):
        # ユーザーがない状態での一覧取得
        response = client.get("/api/v1/users")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_read_users(self, client: TestClient, db_session):
        # ユーザーを作成
        create_test_user_in_db(db_session)

        # ユーザー一覧を取得
        response = client.get("/api/v1/users")
        assert response.status_code == status.HTTP_200_OK
        users = response.json()
        assert len(users) == 1
        assert users[0]["username"] == "testuser"
        assert users[0]["email"] == "test@example.com"

    def test_create_user(self, client: TestClient):
        # 新規ユーザーの作成
        user_data = {
            "email": "new@example.com",
            "username": "newuser",
            "password": "newpassword",
            "manager_id": str(uuid.uuid4()),
            "remarks": "New user",
            "created_by": "test",
            "updated_by": "test",
            "first_name": "New",
            "first_name_ruby": "ニュー",
            "last_name": "User",
            "last_name_ruby": "ユーザー",
            "phone_number": "111-222-3333",
            "zip_code": "111-2222",
            "address": "Kyoto, Japan",
        }

        response = client.post(
            "/api/v1/users",
            content=json.dumps(user_data),
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        created_user = response.json()
        assert created_user["email"] == user_data["email"]
        assert created_user["username"] == user_data["username"]
        assert created_user["first_name"] == user_data["first_name"]
        assert created_user["last_name"] == user_data["last_name"]
        assert "id" in created_user  # IDが生成されていることを確認

    def test_create_user_invalid_email(self, client: TestClient):
        # 無効なメールアドレスでユーザーを作成
        user_data = {
            "email": "invalid-email",  # 無効なメールアドレス
            "username": "invaliduser",
            "password": "password",
            "manager_id": str(uuid.uuid4()),
            "created_by": "test",
            "updated_by": "test",
        }

        response = client.post(
            "/api/v1/users",
            content=json.dumps(user_data),
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid email" in response.json()["detail"]

    def test_get_user(self, client: TestClient, db_session):
        # ユーザーを作成
        user_id = create_test_user_in_db(db_session)

        # 特定のユーザーを取得
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        user = response.json()
        assert user["id"] == user_id
        assert user["username"] == "testuser"
        assert user["email"] == "test@example.com"

    def test_get_user_not_found(self, client: TestClient):
        # 存在しないユーザーIDを使用
        non_existent_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/users/{non_existent_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()

    def test_update_user(self, client: TestClient, db_session):
        # ユーザーを作成
        user_id = create_test_user_in_db(db_session)

        # ユーザー情報を更新
        update_data = {
            "username": "updateduser",
            "remarks": "Updated user information",
            "first_name": "Updated",
            "last_name": "Name",
            "updated_by": "test_updater",
        }

        response = client.put(
            f"/api/v1/users/{user_id}",
            content=json.dumps(update_data),
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == status.HTTP_200_OK
        updated_user = response.json()
        assert updated_user["id"] == user_id
        assert updated_user["username"] == update_data["username"]
        assert updated_user["remarks"] == update_data["remarks"]
        assert updated_user["first_name"] == update_data["first_name"]
        assert updated_user["last_name"] == update_data["last_name"]
        assert updated_user["updated_by"] == update_data["updated_by"]

    def test_update_user_not_found(self, client: TestClient):
        # 存在しないユーザーIDを使用
        non_existent_id = str(uuid.uuid4())
        update_data = {
            "username": "nonexistentuser",
            "updated_by": "test",
        }

        response = client.put(
            f"/api/v1/users/{non_existent_id}",
            content=json.dumps(update_data),
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()

    def test_delete_user(self, client: TestClient, db_session):
        # ユーザーを作成
        user_id = create_test_user_in_db(db_session)

        # ユーザーを削除
        delete_data = {"updated_by": "test_deleter"}
        response = client.delete(
            f"/api/v1/users/{user_id}",
            content=json.dumps(delete_data),
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # 削除後、ユーザーが取得できないことを確認
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_not_found(self, client: TestClient):
        # 存在しないユーザーIDを使用
        non_existent_id = str(uuid.uuid4())
        delete_data = {"updated_by": "test_deleter"}
        response = client.delete(
            f"/api/v1/users/{non_existent_id}",
            content=json.dumps(delete_data),
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()

    # サービスレベルのエラーをテスト
    @patch("app.interfaces.api.v1.endpoints.users.UserService.create_user")
    def test_service_error_handling(
        self, mock_create_user, client: TestClient
    ):
        # サービスレベルでの例外を模擬
        mock_create_user.side_effect = ValueError("Service error")

        user_data = {
            "email": "error@example.com",
            "username": "erroruser",
            "password": "password",
            "manager_id": str(uuid.uuid4()),
            "created_by": "test",
            "updated_by": "test",
        }

        response = client.post(
            "/api/v1/users",
            content=json.dumps(user_data),
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Service error" in response.json()["detail"]
