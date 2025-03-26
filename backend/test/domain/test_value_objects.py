import uuid

import pytest

from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId


class TestEmail:
    def test_valid_email(self):
        # 正常なメールアドレスを検証
        email = Email("test@example.com")
        assert str(email) == "test@example.com"

        email = Email("user.name+tag@domain.co.jp")
        assert str(email) == "user.name+tag@domain.co.jp"

    def test_invalid_email(self):
        # 無効なメールアドレスを検証
        with pytest.raises(ValueError):
            Email("")

        with pytest.raises(ValueError):
            Email("invalid-email")

        with pytest.raises(ValueError):
            Email("user@")

        with pytest.raises(ValueError):
            Email("@domain.com")

        with pytest.raises(ValueError):
            Email("user@domain")

    def test_equality(self):
        # 同じ値を持つEmailオブジェクトは等価である
        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        assert email1 == email2

        # 大文字小文字は区別されるため、異なるオブジェクトとなる
        email3 = Email("Test@example.com")
        assert email1 != email3


class TestUserId:
    def test_create_from_string(self):
        # 文字列からUserIdを作成
        user_id_str = "a7d64a0d-c57d-4b8e-b5b8-2b1b25d54485"
        user_id = UserId(user_id_str)
        assert str(user_id) == user_id_str
        assert isinstance(user_id.value, uuid.UUID)

    def test_create_from_uuid(self):
        # UUIDからUserIdを作成
        uuid_obj = uuid.uuid4()
        user_id = UserId(uuid_obj)
        assert str(user_id) == str(uuid_obj)
        assert user_id.value == uuid_obj

    def test_generate(self):
        # 新しいUserIdを生成
        user_id = UserId.generate()
        assert isinstance(user_id, UserId)
        assert isinstance(user_id.value, uuid.UUID)

    def test_invalid_user_id(self):
        # 無効なUUID形式の文字列
        with pytest.raises(ValueError):
            UserId("not-a-uuid")

    def test_equality(self):
        # 同一のUUIDを持つUserIdは等価
        uuid_str = "a7d64a0d-c57d-4b8e-b5b8-2b1b25d54485"
        user_id1 = UserId(uuid_str)
        user_id2 = UserId(uuid_str)
        assert user_id1 == user_id2

        # 異なるUUIDは等価でない
        user_id3 = UserId.generate()
        assert user_id1 != user_id3
