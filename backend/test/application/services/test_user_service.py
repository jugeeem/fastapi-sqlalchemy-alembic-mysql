# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザーサービステストモジュール

このモジュールでは、UserServiceクラスの機能をテストします。
ユーザー作成、重複チェック、パスワードハッシュ化などの機能を検証します。
"""

import uuid
from datetime import date, datetime
from unittest.mock import MagicMock

import pytest
from passlib.context import CryptContext

from app.application.dtos.user_dto import UserCreateDTO
from app.application.services.user_service import UserService
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.enums import Gender


class TestUserService:
    """UserServiceのテストクラス

    UserServiceの各メソッドの機能を検証します。
    ユーザー作成、バリデーション、エラー処理などをテストします。
    """

    @pytest.fixture
    def mock_user_repository(self):
        """モックユーザーリポジトリのフィクスチャ

        UserRepositoryをモック化し、テストで使用するためのフィクスチャを提供します。

        Returns:
            MagicMock: モック化されたUserRepositoryインスタンス
        """
        mock_repo = MagicMock(spec=UserRepository)
        mock_repo.find_by_username.return_value = None
        mock_repo.find_by_email.return_value = None
        mock_repo.get_default_user_role_id.return_value = uuid.uuid4()

        # createメソッドが呼ばれたとき、引数をそのまま返すようにする
        mock_repo.create.side_effect = lambda user: self._mock_create_user(
            user
        )

        return mock_repo

    def _mock_create_user(self, user: User) -> User:
        """モックのcreateメソッド実装

        UserRepositoryのcreateメソッドのモック実装です。
        ユーザーエンティティにIDや作成日時などを設定して返します。

        Args:
            user (User): 作成するユーザーエンティティ

        Returns:
            User: 作成されたユーザーエンティティ（ID等が設定された状態）
        """
        user.id = uuid.uuid4()
        user.created_at = datetime.now()
        user.updated_at = datetime.now()
        user.created_by = "system"
        user.updated_by = "system"
        return user

    @pytest.fixture
    def valid_user_dto(self):
        """有効なユーザーDTOのフィクスチャ

        テスト用の有効なUserCreateDTOを提供します。

        Returns:
            UserCreateDTO: 有効なユーザー作成DTO
        """
        return UserCreateDTO(
            username="testuser",
            email="test@example.com",
            password="password123",
            first_name="Test",
            first_name_ruby="テスト",
            last_name="User",
            last_name_ruby="ユーザー",
            gender=Gender.MALE,
            birth_day=date(2000, 1, 1),
            phone_number="090-1234-5678",
            zip_code="123-4567",
            address="Tokyo, Japan",
        )

    def test_create_user_success(self, mock_user_repository, valid_user_dto):
        """ユーザー作成の成功ケースをテスト

        有効なDTOを使用して、ユーザーが正常に作成されることを確認します。

        Args:
            mock_user_repository: モックユーザーリポジトリ
            valid_user_dto: 有効なユーザーDTO
        """
        # UserServiceのインスタンス化
        service = UserService(mock_user_repository)

        # ユーザー作成
        response = service.create_user(valid_user_dto)

        # 検証
        assert response.username == valid_user_dto.username
        assert response.email == valid_user_dto.email
        assert response.id is not None
        assert response.created_at is not None
        assert response.created_by == "system"

        # リポジトリのメソッドが正しく呼ばれたことを確認
        mock_user_repository.find_by_username.assert_called_once_with(
            valid_user_dto.username
        )
        mock_user_repository.find_by_email.assert_called_once_with(
            valid_user_dto.email
        )
        mock_user_repository.get_default_user_role_id.assert_called_once()
        mock_user_repository.create.assert_called_once()

    def test_create_user_username_already_exists(
        self, mock_user_repository, valid_user_dto
    ):
        """既存ユーザー名によるエラーケースをテスト

        既に存在するユーザー名で作成を試みた場合に、適切なエラーが発生することを確認します。

        Args:
            mock_user_repository: モックユーザーリポジトリ
            valid_user_dto: 有効なユーザーDTO
        """
        # ユーザー名が既に存在する状況をモック
        existing_user = User(
            id=uuid.uuid4(),
            username=valid_user_dto.username,
            email="existing@example.com",
        )
        mock_user_repository.find_by_username.return_value = existing_user

        # UserServiceのインスタンス化
        service = UserService(mock_user_repository)

        # エラーが発生することを確認
        with pytest.raises(ValueError) as exc_info:
            service.create_user(valid_user_dto)

        # エラーメッセージを確認
        assert f"Username {valid_user_dto.username} already exists" in str(
            exc_info.value
        )

    def test_create_user_email_already_exists(
        self, mock_user_repository, valid_user_dto
    ):
        """既存メールアドレスによるエラーケースをテスト

        既に存在するメールアドレスで作成を試みた場合に、適切なエラーが発生することを確認します。

        Args:
            mock_user_repository: モックユーザーリポジトリ
            valid_user_dto: 有効なユーザーDTO
        """
        # メールアドレスが既に存在する状況をモック
        existing_user = User(
            id=uuid.uuid4(),
            username="existinguser",
            email=valid_user_dto.email,
        )
        mock_user_repository.find_by_username.return_value = None
        mock_user_repository.find_by_email.return_value = existing_user

        # UserServiceのインスタンス化
        service = UserService(mock_user_repository)

        # エラーが発生することを確認
        with pytest.raises(ValueError) as exc_info:
            service.create_user(valid_user_dto)

        # エラーメッセージを確認
        assert f"Email {valid_user_dto.email} already exists" in str(
            exc_info.value
        )

    def test_password_hashing(self, mock_user_repository, valid_user_dto):
        """パスワードハッシュ化機能をテスト

        パスワードが適切にハッシュ化されることを確認します。

        Args:
            mock_user_repository: モックユーザーリポジトリ
            valid_user_dto: 有効なユーザーDTO
        """
        # UserServiceのインスタンス化
        service = UserService(mock_user_repository)

        # パスワードをハッシュ化
        hashed_password = service._get_password_hash(valid_user_dto.password)

        # パスワードがハッシュ化されていることを確認
        assert hashed_password != valid_user_dto.password

        # ハッシュが正しい形式であることを確認
        # bcryptハッシュは通常'$2b$'で始まる
        assert hashed_password.startswith("$2")

        # ハッシュが元のパスワードを検証できることを確認
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        assert pwd_context.verify(valid_user_dto.password, hashed_password)

    def test_create_user_with_role_assignment(
        self, mock_user_repository, valid_user_dto
    ):
        """ロール割り当て機能をテスト

        ユーザー作成時にデフォルトロールが正しく割り当てられることを確認します。

        Args:
            mock_user_repository: モックユーザーリポジトリ
            valid_user_dto: 有効なユーザーDTO
        """
        # デフォルトロールIDを設定
        default_role_id = uuid.uuid4()
        mock_user_repository.get_default_user_role_id.return_value = (
            default_role_id
        )

        # UserServiceのインスタンス化
        service = UserService(mock_user_repository)

        # ユーザー作成
        response = service.create_user(valid_user_dto)

        # ロールが正しく割り当てられたことを確認
        assert len(response.role_ids) == 1
        assert response.role_ids[0] == default_role_id

        # create呼び出し時の引数を取得
        created_user_arg = mock_user_repository.create.call_args[0][0]

        # 作成されたユーザーエンティティにロールIDが設定されていることを確認
        assert len(created_user_arg.role_ids) == 1
        assert created_user_arg.role_ids[0] == default_role_id
