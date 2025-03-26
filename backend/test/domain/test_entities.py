from datetime import datetime

import pytest

from app.domain.entities.user import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId


class TestUserEntity:
    @pytest.fixture
    def sample_user(self):
        return User(
            id=UserId.generate(),
            email=Email("test@example.com"),
            username="testuser",
            password="password123",
            manager_id="00000000-0000-0000-0000-000000000000",
            remarks="Test user",
            delete_flag=False,
            created_at=datetime.now(),
            created_by="system",
            updated_at=datetime.now(),
            updated_by="system",
            first_name="Test",
            last_name="User",
            first_name_ruby="テスト",
            last_name_ruby="ユーザー",
            phone_number="123-456-7890",
            zip_code="123-4567",
            address="Tokyo, Japan",
        )

    def test_user_creation(self, sample_user):
        # ユーザーエンティティが正しく作成されることを検証
        assert isinstance(sample_user.id, UserId)
        assert isinstance(sample_user.email, Email)
        assert sample_user.username == "testuser"
        assert sample_user.password == "password123"
        assert sample_user.delete_flag is False
        assert sample_user.first_name == "Test"
        assert sample_user.last_name == "User"

    def test_activate_user(self, sample_user):
        # 削除されたユーザーをアクティブ化
        deactivated_user = User(
            id=sample_user.id,
            email=sample_user.email,
            username=sample_user.username,
            password=sample_user.password,
            manager_id=sample_user.manager_id,
            remarks=sample_user.remarks,
            delete_flag=True,  # 削除フラグを True に設定
            created_at=sample_user.created_at,
            created_by=sample_user.created_by,
            updated_at=sample_user.updated_at,
            updated_by=sample_user.updated_by,
            first_name=sample_user.first_name,
            first_name_ruby=sample_user.first_name_ruby,
            last_name=sample_user.last_name,
            last_name_ruby=sample_user.last_name_ruby,
            phone_number=sample_user.phone_number,
            zip_code=sample_user.zip_code,
            address=sample_user.address,
        )

        # アクティブ化
        activated_user = deactivated_user.activate()
        assert activated_user.delete_flag is False
        assert activated_user.id == deactivated_user.id
        assert activated_user.email == deactivated_user.email
        assert activated_user.updated_at > deactivated_user.updated_at

    def test_deactivate_user(self, sample_user):
        # ユーザーの非アクティブ化（論理削除）
        deactivated_user = sample_user.deactivate()
        assert deactivated_user.delete_flag is True
        assert deactivated_user.id == sample_user.id
        assert deactivated_user.email == sample_user.email
        assert deactivated_user.updated_at > sample_user.updated_at

    def test_update_username(self, sample_user):
        # ユーザー名の更新
        new_username = "updateduser"
        updated_user = sample_user.update_username(new_username)
        assert updated_user.username == new_username
        assert updated_user.id == sample_user.id
        assert updated_user.email == sample_user.email
        assert updated_user.updated_at > sample_user.updated_at
