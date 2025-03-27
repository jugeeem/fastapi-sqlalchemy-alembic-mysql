import uuid
from datetime import datetime
from typing import Dict, Generator, List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId
from app.infrastructure.database import Base, get_db
from app.main import app

# インメモリSQLiteデータベースを使用
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# テスト用のデータベースセッションを提供するオーバーライド関数
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# テスト用にDBの依存関係をオーバーライド
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def test_db():
    # テスト開始前にテーブルを作成
    Base.metadata.create_all(bind=engine)
    yield
    # テスト後にテーブルを削除
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(test_db) -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


# モック用のユーザーリポジトリクラス
class MockUserRepository(UserRepository):
    def __init__(self):
        self.users: Dict[str, User] = {}

    def find_by_id(self, user_id: UserId) -> User:
        return self.users.get(str(user_id))

    def find_by_email(self, email: Email) -> User:
        for user in self.users.values():
            if str(user.email) == str(email):
                return user
        return None

    def find_all(
        self, limit=None, offset=None, order_by=None, asc=True
    ) -> List[User]:
        users = list(self.users.values())
        if order_by:
            users.sort(key=lambda u: getattr(u, order_by), reverse=not asc)
        if offset:
            users = users[offset:]
        if limit:
            users = users[:limit]
        return users

    def create(self, user: User) -> User:
        """新しいユーザーを作成する。

        Args:
            user: 作成するUserエンティティ。

        Returns:
            作成されたUserエンティティ。
        """
        # ユーザーが既に存在していないことを確認
        if str(user.id) in self.users:
            raise ValueError(f"User with ID {user.id} already exists")

        # ユーザーを辞書に追加
        self.users[str(user.id)] = user
        return user

    def update(self, user: User) -> User:
        """既存のユーザーを更新する。

        Args:
            user: 更新するUserエンティティ。

        Returns:
            更新されたUserエンティティ。

        Raises:
            ValueError: ユーザーが存在しない場合。
        """
        # ユーザーが存在することを確認
        if str(user.id) not in self.users:
            raise ValueError(f"User with ID {user.id} not found")

        # ユーザー情報を更新
        self.users[str(user.id)] = user
        return user

    def delete(self, user_id: UserId) -> None:
        if str(user_id) in self.users:
            # 実際の実装では論理削除するため、ここではユーザーを変更して保存
            user = self.users[str(user_id)]
            self.users[str(user_id)] = User(
                id=user.id,
                email=user.email,
                username=user.username,
                password=user.password,
                manager_id=user.manager_id,
                remarks=user.remarks,
                delete_flag=True,  # 削除フラグをTrueに設定
                created_at=user.created_at,
                created_by=user.created_by,
                updated_at=datetime.now(),
                updated_by="test_user",
                first_name=user.first_name,
                first_name_ruby=user.first_name_ruby,
                last_name=user.last_name,
                last_name_ruby=user.last_name_ruby,
                phone_number=user.phone_number,
                zip_code=user.zip_code,
                address=user.address,
            )


@pytest.fixture
def mock_user_repository() -> MockUserRepository:
    return MockUserRepository()


@pytest.fixture
def sample_user_id() -> UserId:
    return UserId("a7d64a0d-c57d-4b8e-b5b8-2b1b25d54485")


@pytest.fixture
def sample_user(sample_user_id) -> User:
    return User(
        id=sample_user_id,
        email=Email("test@example.com"),
        username="testuser",
        password="password123",
        manager_id=str(uuid.uuid4()),
        remarks="Test remarks",
        delete_flag=False,
        created_at=datetime.now(),
        created_by="system",
        updated_at=datetime.now(),
        updated_by="system",
        first_name="Test",
        first_name_ruby="テスト",
        last_name="User",
        last_name_ruby="ユーザー",
        phone_number="123-456-7890",
        zip_code="123-4567",
        address="Tokyo, Japan",
    )
