from datetime import date
from unittest.mock import Mock, patch

import pytest

from app.application.dtos.user_dto import UserCreateDTO
from app.application.services.user_service import UserService
from app.domain.entities.user import User
from app.domain.value_objects.enums import Gender


@pytest.fixture
def mock_user_repository():
    """UserRepositoryのモックを作成するフィクスチャ"""
    repository = Mock()
    # デフォルトの戻り値設定
    repository.find_by_username.return_value = None
    repository.find_by_email.return_value = None
    repository.get_default_user_role_id.return_value = 1

    # ユーザー作成時のモック
    def create_mock(user):
        # created_atとupdated_atも設定されるため、モックで返すオブジェクトを補完
        user.id = 1
        user.created_at = "2023-01-01T00:00:00"
        user.updated_at = "2023-01-01T00:00:00"
        return user

    repository.create.side_effect = create_mock
    return repository


@pytest.fixture
def user_service(mock_user_repository):
    """テスト用のUserServiceインスタンスを作成するフィクスチャ"""
    return UserService(mock_user_repository)


@pytest.fixture
def valid_user_dto():
    """有効なユーザー作成DTOを返すフィクスチャ"""
    return UserCreateDTO(
        username="testuser",
        email="test@example.com",
        password="password123",
        first_name="太郎",
        first_name_ruby="たろう",
        last_name="山田",
        last_name_ruby="やまだ",
        gender=Gender.MALE,
        birth_day=date(1990, 1, 1),
        phone_number="090-1234-5678",
        zip_code="123-4567",
        address="東京都渋谷区",
    )


def test_create_user_success(
    user_service, mock_user_repository, valid_user_dto
):
    """ユーザー作成が成功するケースのテスト"""
    # テスト実行
    response = user_service.create_user(valid_user_dto)

    # 検証
    assert response.id == 1
    assert response.username == valid_user_dto.username
    assert response.email == valid_user_dto.email
    assert response.first_name == valid_user_dto.first_name

    # リポジトリのメソッドが正しく呼ばれたことを検証
    mock_user_repository.find_by_username.assert_called_once_with(
        valid_user_dto.username
    )
    mock_user_repository.find_by_email.assert_called_once_with(
        valid_user_dto.email
    )
    mock_user_repository.get_default_user_role_id.assert_called_once()
    mock_user_repository.create.assert_called_once()


def test_create_user_duplicate_username(
    user_service, mock_user_repository, valid_user_dto
):
    """ユーザー名が既に存在する場合のテスト"""
    # リポジトリの戻り値を設定してユーザー名が既に存在する状況を作る
    mock_user_repository.find_by_username.return_value = User(
        id=2, username=valid_user_dto.username
    )

    # ValueErrorが発生することを検証
    with pytest.raises(ValueError) as exc_info:
        user_service.create_user(valid_user_dto)

    assert f"Username {valid_user_dto.username} already exists" in str(
        exc_info.value
    )
    # create()メソッドが呼ばれていないことを検証
    mock_user_repository.create.assert_not_called()


def test_create_user_duplicate_email(
    user_service, mock_user_repository, valid_user_dto
):
    """メールアドレスが既に存在する場合のテスト"""
    # リポジトリの戻り値を設定してメールアドレスが既に存在する状況を作る
    mock_user_repository.find_by_email.return_value = User(
        id=2, email=valid_user_dto.email
    )

    # ValueErrorが発生することを検証
    with pytest.raises(ValueError) as exc_info:
        user_service.create_user(valid_user_dto)

    assert f"Email {valid_user_dto.email} already exists" in str(
        exc_info.value
    )
    # create()メソッドが呼ばれていないことを検証
    mock_user_repository.create.assert_not_called()


def test_password_hashing(user_service):
    """パスワードのハッシュ化が正しく行われることを検証"""
    # 平文パスワード
    plain_password = "test_password"

    # ハッシュ化されたパスワードを取得
    hashed_password = user_service._get_password_hash(plain_password)

    # 検証
    assert plain_password != hashed_password
    assert len(hashed_password) > 0

    # CryptContextのpatchを使用して検証する方法も可能
    with patch(
        "app.application.services.user_service.pwd_context"
    ) as mock_pwd_context:
        mock_pwd_context.hash.return_value = "hashed_password"
        result = user_service._get_password_hash(plain_password)
        assert result == "hashed_password"
        mock_pwd_context.hash.assert_called_once_with(plain_password)
