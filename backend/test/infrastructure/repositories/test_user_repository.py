# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザーリポジトリテストモジュール

このモジュールでは、SQLAlchemyUserRepositoryの実装に対するテストケースを定義します。
ユーザーの作成、検索、デフォルトロールの取得などの機能を検証します。
"""

import pytest
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.value_objects.enums import Gender, Role
from app.infrastructure.models.role import RoleModel
from app.infrastructure.repositories.user_repository import (
    SQLAlchemyUserRepository,
)


class TestSQLAlchemyUserRepository:
    """SQLAlchemyUserRepositoryのテストクラス

    ユーザーリポジトリの各メソッドの動作を検証するためのテストケースを提供します。
    """

    def test_create_user_success(self, db: Session):
        """ユーザー作成の成功ケースをテスト

        有効なユーザーエンティティが正常に作成され、適切な情報が設定されることを確認します。

        Args:
            db (Session): テスト用データベースセッション
        """
        # テスト用のロールを作成
        role = RoleModel(
            name=Role.USER.value,
            description="Test Role",
            created_by="system",
            updated_by="system",
        )
        db.add(role)
        db.commit()
        db.refresh(role)

        # リポジトリのインスタンス化
        repo = SQLAlchemyUserRepository(db)

        # テスト用ユーザーエンティティの作成
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password_here",
            first_name="Test",
            first_name_ruby="テスト",
            last_name="User",
            last_name_ruby="ユーザー",
            gender=Gender.MALE,
            birth_day="2000-01-01",
            phone_number="090-1234-5678",
            zip_code="123-4567",
            address="Tokyo, Japan",
            role_ids=[role.id],
        )

        # ユーザー作成
        created_user = repo.create(test_user)

        # 検証
        assert created_user.id is not None
        assert created_user.username == "testuser"
        assert created_user.email == "test@example.com"
        assert created_user.created_at is not None
        assert created_user.created_by == "system"
        assert len(created_user.role_ids) == 1

        # データベースに保存されたことを確認
        db_user = repo.find_by_username("testuser")
        assert db_user is not None
        assert db_user.email == "test@example.com"

    def test_find_by_username_existing(self, db: Session):
        """既存ユーザー名でのユーザー検索をテスト

        存在するユーザー名でユーザーが正しく検索できることを確認します。

        Args:
            db (Session): テスト用データベースセッション
        """
        # テスト用のロールを作成
        role = RoleModel(
            name=Role.USER.value,
            description="Test Role",
            created_by="system",
            updated_by="system",
        )
        db.add(role)
        db.commit()

        # リポジトリのインスタンス化
        repo = SQLAlchemyUserRepository(db)

        # テスト用ユーザーの作成
        test_user = User(
            username="findbyuser",
            email="findby@example.com",
            hashed_password="hashed_password_here",
            gender=Gender.MALE,
            birth_day="2000-01-01",
            role_ids=[role.id],
        )
        repo.create(test_user)

        # 検索
        found_user = repo.find_by_username("findbyuser")

        # 検証
        assert found_user is not None
        assert found_user.username == "findbyuser"
        assert found_user.email == "findby@example.com"

    def test_find_by_username_nonexistent(self, db: Session):
        """存在しないユーザー名での検索をテスト

        存在しないユーザー名でNoneが返されることを確認します。

        Args:
            db (Session): テスト用データベースセッション
        """
        # リポジトリのインスタンス化
        repo = SQLAlchemyUserRepository(db)

        # 検索
        found_user = repo.find_by_username("nonexistentuser")

        # 検証
        assert found_user is None

    def test_find_by_email_existing(self, db: Session):
        """既存メールアドレスでのユーザー検索をテスト

        存在するメールアドレスでユーザーが正しく検索できることを確認します。

        Args:
            db (Session): テスト用データベースセッション
        """
        # テスト用のロールを作成
        role = RoleModel(
            name=Role.USER.value,
            description="Test Role",
            created_by="system",
            updated_by="system",
        )
        db.add(role)
        db.commit()

        # リポジトリのインスタンス化
        repo = SQLAlchemyUserRepository(db)

        # テスト用ユーザーの作成
        test_user = User(
            username="emailuser",
            email="find_email@example.com",
            hashed_password="hashed_password_here",
            gender=Gender.MALE,
            birth_day="2000-01-01",
            role_ids=[role.id],
        )
        repo.create(test_user)

        # 検索
        found_user = repo.find_by_email("find_email@example.com")

        # 検証
        assert found_user is not None
        assert found_user.username == "emailuser"
        assert found_user.email == "find_email@example.com"

    def test_find_by_email_nonexistent(self, db: Session):
        """存在しないメールアドレスでの検索をテスト

        存在しないメールアドレスでNoneが返されることを確認します。

        Args:
            db (Session): テスト用データベースセッション
        """
        # リポジトリのインスタンス化
        repo = SQLAlchemyUserRepository(db)

        # 検索
        found_user = repo.find_by_email("nonexistent@example.com")

        # 検証
        assert found_user is None

    def test_get_default_user_role_id(self, db: Session):
        """デフォルトユーザーロールIDの取得をテスト

        USERロールのIDが正しく取得できることを確認します。

        Args:
            db (Session): テスト用データベースセッション
        """
        # テスト用のロールを作成
        role = RoleModel(
            name=Role.USER.value,
            description="Default User Role",
            created_by="system",
            updated_by="system",
        )
        db.add(role)
        db.commit()
        db.refresh(role)

        # リポジトリのインスタンス化
        repo = SQLAlchemyUserRepository(db)

        # デフォルトロールID取得
        role_id = repo.get_default_user_role_id()

        # 検証
        assert role_id is not None
        assert role_id == role.id

    def test_get_default_user_role_id_not_found(self, db: Session):
        """デフォルトユーザーロールが存在しない場合のエラーをテスト

        USERロールが存在しない場合にValueErrorが発生することを確認します。

        Args:
            db (Session): テスト用データベースセッション
        """
        # リポジトリのインスタンス化
        repo = SQLAlchemyUserRepository(db)

        # USERロールが存在しない場合はValueErrorが発生することを確認
        with pytest.raises(ValueError):
            repo.get_default_user_role_id()
