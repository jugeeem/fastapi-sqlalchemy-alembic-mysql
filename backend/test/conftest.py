# !/usr/bin/python
# -*- coding: utf-8 -*-
"""テスト設定モジュール

このモジュールでは、pytestのための共通設定とフィクスチャを定義します。
テストデータベースの設定、モックリポジトリの実装、
テストクライアントの作成など、テストに必要な基本的な機能を提供します。
"""

import uuid
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.enums import Gender, Role
from app.infrastructure.database import Base, get_db
from app.infrastructure.models.role import RoleModel
from app.main import app

# テスト用のインメモリデータベースを設定
TEST_DATABASE_URL = "mysql+pymysql://user:password@test-db:3306/app_db"
engine = create_engine(
    TEST_DATABASE_URL,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# Mock UserRepository class
class MockUserRepository(UserRepository):
    """モックユーザーリポジトリクラス

    テスト用のユーザーリポジトリの実装です。
    実際のデータベースの代わりにインメモリのデータ構造を使用して、
    ユーザーの作成や検索機能を提供します。

    Attributes:
        db_session (Session): SQLAlchemyデータベースセッション
        users (dict): ユーザーIDをキーとするユーザーエンティティの辞書
    """

    def __init__(self, db_session: Session):
        """モックリポジトリの初期化

        Args:
            db_session (Session): SQLAlchemyデータベースセッション
        """
        self.db_session = db_session
        self.users = {}

    def create(self, user: User) -> User:
        """ユーザーを作成する

        Args:
            user (User): 作成するユーザーエンティティ

        Returns:
            User: 作成されたユーザーエンティティ（ID等が設定された状態）
        """
        user_id = uuid.uuid4()
        user.id = user_id
        user.created_at = "2023-01-01T00:00:00"
        user.updated_at = "2023-01-01T00:00:00"
        user.created_by = "system"
        user.updated_by = "system"
        self.users[str(user_id)] = user
        return user

    def find_by_username(self, username: str):
        """ユーザー名でユーザーを検索する

        Args:
            username (str): 検索するユーザー名

        Returns:
            User: 見つかったユーザーエンティティ、見つからない場合はNone
        """
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def find_by_email(self, email: str):
        """メールアドレスでユーザーを検索する

        Args:
            email (str): 検索するメールアドレス

        Returns:
            User: 見つかったユーザーエンティティ、見つからない場合はNone
        """
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def get_default_user_role_id(self):
        """デフォルトのユーザーロールIDを取得する

        Returns:
            UUID: ランダムに生成されたUUID（テスト用）
        """
        return uuid.uuid4()


@pytest.fixture(scope="function")
def db() -> Generator:
    """テスト用データベースセッションを提供するフィクスチャ

    テスト用のデータベースを設定し、テスト実行中はトランザクション内で
    操作を行い、テスト終了後はロールバックします。

    Yields:
        Session: テスト用のSQLAlchemyセッション
    """
    # テスト用データベースのセットアップ
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    # テスト終了後のクリーンアップ
    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def init_roles(db: Session) -> None:
    """テスト用のロールを初期化するフィクスチャ

    テストデータベースに標準的なロール（ADMIN、MANAGER、USER、GUEST）を
    作成します。

    Args:
        db (Session): データベースセッション

    Returns:
        None
    """
    roles = [
        RoleModel(
            name=Role.ADMIN.value,
            description="Administrator",
            created_by="system",
            updated_by="system",
        ),
        RoleModel(
            name=Role.MANAGER.value,
            description="Manager",
            created_by="system",
            updated_by="system",
        ),
        RoleModel(
            name=Role.USER.value,
            description="Regular User",
            created_by="system",
            updated_by="system",
        ),
        RoleModel(
            name=Role.GUEST.value,
            description="Guest User",
            created_by="system",
            updated_by="system",
        ),
    ]
    db.add_all(roles)
    db.commit()

    # ロールIDを確認
    for role in db.query(RoleModel).all():
        print(f"Role created: {role.name}, ID: {role.id}")

    return None


@pytest.fixture(scope="function")
def client(db: Session, init_roles: None) -> Generator:
    """テスト用APIクライアントを提供するフィクスチャ

    FastAPIのテストクライアントを作成し、テスト用データベースセッションを
    注入します。

    Args:
        db (Session): データベースセッション
        init_roles (None): 初期化されたロール

    Yields:
        TestClient: FastAPIのテストクライアント
    """

    # テスト用のAPIクライアントとDBセッションを設定
    def _get_test_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def valid_user_data() -> Dict:
    """有効なユーザーデータを提供するフィクスチャ

    テスト用の有効なユーザーデータを辞書形式で返します。

    Returns:
        Dict: 有効なユーザーデータの辞書
    """
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "first_name_ruby": "テスト",
        "last_name": "User",
        "last_name_ruby": "ユーザー",
        "gender": Gender.MALE.value,
        "birth_day": "2000-01-01",
        "phone_number": "090-1234-5678",
        "zip_code": "123-4567",
        "address": "Tokyo, Japan",
    }
