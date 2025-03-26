import uuid
from datetime import datetime

import pytest

from app.application.dtos.user_dto import UserCreateDTO, UserUpdateDTO
from app.application.services.user_service import UserService
from app.domain.entities.user import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId


class TestUserService:
    def test_get_user(self, mock_user_repository, sample_user):
        # リポジトリにユーザーを追加
        mock_user_repository.save(sample_user)
        service = UserService(mock_user_repository)

        # ユーザーの取得をテスト
        user_dto = service.get_user(str(sample_user.id))
        assert user_dto is not None
        assert user_dto.id == str(sample_user.id)
        assert user_dto.email == str(sample_user.email)
        assert user_dto.username == sample_user.username

    def test_get_user_not_found(self, mock_user_repository):
        service = UserService(mock_user_repository)
        user_dto = service.get_user(str(uuid.uuid4()))
        assert user_dto is None

    def test_get_users(self, mock_user_repository, sample_user):
        # 複数ユーザーをリポジトリに追加
        mock_user_repository.save(sample_user)

        another_user = User(
            id=UserId.generate(),
            email=Email("another@example.com"),
            username="anotheruser",
            password="password456",
            manager_id=str(uuid.uuid4()),
            remarks="Another test user",
            delete_flag=False,
            created_at=datetime.now(),
            created_by="system",
            updated_at=datetime.now(),
            updated_by="system",
            first_name="Another",
            first_name_ruby="アナザー",
            last_name="User",
            last_name_ruby="ユーザー",
            phone_number="098-765-4321",
            zip_code="987-6543",
            address="Osaka, Japan",
        )
        mock_user_repository.save(another_user)

        service = UserService(mock_user_repository)

        # 全ユーザーの取得
        users = service.get_users()
        assert len(users) == 2

        # 制限付きの取得
        limited_users = service.get_users(limit=1)
        assert len(limited_users) == 1

    def test_create_user(self, mock_user_repository):
        service = UserService(mock_user_repository)

        # ユーザー作成DTO
        user_create_dto = UserCreateDTO(
            email="new@example.com",
            username="newuser",
            password="newpassword",
            manager_id=str(uuid.uuid4()),
            remarks="New user",
            created_by="test",
            updated_by="test",
            first_name="New",
            first_name_ruby="ニュー",
            last_name="User",
            last_name_ruby="ユーザー",
            phone_number="111-222-3333",
            zip_code="111-2222",
            address="Kyoto, Japan",
        )

        # ユーザー作成
        created_user = service.create_user(user_create_dto)
        assert created_user is not None
        assert created_user.email == user_create_dto.email
        assert created_user.username == user_create_dto.username
        assert created_user.first_name == user_create_dto.first_name
        assert created_user.last_name == user_create_dto.last_name

        # 作成したユーザーがリポジトリに保存されていることを確認
        user = mock_user_repository.find_by_email(Email(user_create_dto.email))
        assert user is not None
        assert str(user.email) == user_create_dto.email

    def test_create_user_duplicate_email(
        self, mock_user_repository, sample_user
    ):
        # 既存ユーザーの保存
        mock_user_repository.save(sample_user)
        service = UserService(mock_user_repository)

        # 同じメールアドレスで新しいユーザーを作成しようとする
        user_create_dto = UserCreateDTO(
            email=str(sample_user.email),  # 既存ユーザーと同じメールアドレス
            username="duplicateuser",
            password="password",
            manager_id=str(uuid.uuid4()),
            remarks="Duplicate user",
            created_by="test",
            updated_by="test",
        )

        # 重複エラーが発生することを検証
        with pytest.raises(
            ValueError, match=r"User with email .* already exists"
        ):
            service.create_user(user_create_dto)

    def test_update_user(self, mock_user_repository, sample_user):
        # ユーザーの保存
        mock_user_repository.save(sample_user)
        service = UserService(mock_user_repository)

        # 更新データ
        user_update_dto = UserUpdateDTO(
            username="updatedusername",
            remarks="Updated remarks",
            first_name="Updated",
            last_name="Name",
            updated_by="test",
        )

        # ユーザーの更新
        updated_user = service.update_user(
            str(sample_user.id), user_update_dto
        )
        assert updated_user is not None
        assert updated_user.username == user_update_dto.username
        assert updated_user.remarks == user_update_dto.remarks
        assert updated_user.first_name == user_update_dto.first_name
        assert updated_user.last_name == user_update_dto.last_name
        assert updated_user.id == str(sample_user.id)
        assert updated_user.email == str(sample_user.email)

    def test_update_user_not_found(self, mock_user_repository):
        service = UserService(mock_user_repository)
        update_dto = UserUpdateDTO(username="notfound", updated_by="test")
        updated_user = service.update_user(str(uuid.uuid4()), update_dto)
        assert updated_user is None

    def test_delete_user(self, mock_user_repository, sample_user):
        # ユーザーの保存
        mock_user_repository.save(sample_user)
        service = UserService(mock_user_repository)

        # ユーザーの削除
        result = service.delete_user(str(sample_user.id))
        assert result is True

        # 削除されたユーザーを取得
        user = mock_user_repository.find_by_id(sample_user.id)
        assert user.delete_flag is True

    def test_delete_user_not_found(self, mock_user_repository):
        service = UserService(mock_user_repository)
        result = service.delete_user(str(uuid.uuid4()))
        assert result is False
