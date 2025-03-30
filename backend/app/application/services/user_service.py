# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザーサービスモジュール

このモジュールでは、ユーザー関連のビジネスロジックを実装するサービスを定義します。
ドメイン層とインターフェース層の間の中間層として機能し、
ユーザーの作成、認証、更新などの操作を行います。
"""

from passlib.context import CryptContext

from app.application.dtos.user_dto import UserCreateDTO, UserResponseDTO
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """ユーザー関連のビジネスロジックを実装するサービスクラス

    ユーザーの作成、取得、更新、削除などのユースケースを実装します。
    DTOとドメインエンティティの変換、パスワードのハッシュ化、
    ユーザー情報の検証などを担当します。

    Attributes:
        user_repository (UserRepository): ユーザーリポジトリのインスタンス
    """

    def __init__(self, user_repository: UserRepository):
        """UserServiceの初期化

        Args:
            user_repository (UserRepository): ユーザーリポジトリのインスタンス
        """
        self.user_repository = user_repository

    def create_user(self, user_dto: UserCreateDTO) -> UserResponseDTO:
        """新規ユーザーを作成する

        ユーザー作成DTOを受け取り、バリデーション後にユーザーエンティティを作成し、
        リポジトリに保存します。作成されたユーザー情報をDTOに変換して返します。

        Args:
            user_dto (UserCreateDTO): ユーザー作成リクエストDTO

        Returns:
            UserResponseDTO: 作成されたユーザー情報を含むレスポンスDTO

        Raises:
            ValueError: ユーザー名またはメールアドレスが既に存在する場合
        """
        # ユーザー名やメールアドレスの重複チェック
        if self.user_repository.find_by_username(user_dto.username):
            raise ValueError(f"Username {user_dto.username} already exists")

        if self.user_repository.find_by_email(user_dto.email):
            raise ValueError(f"Email {user_dto.email} already exists")

        # パスワードをハッシュ化
        hashed_password = self._get_password_hash(user_dto.password)

        # デフォルトのユーザー権限IDを取得
        default_role_id = self.user_repository.get_default_user_role_id()

        # ユーザーエンティティを作成
        user = User(
            username=user_dto.username,
            email=user_dto.email,
            hashed_password=hashed_password,
            first_name=user_dto.first_name,
            first_name_ruby=user_dto.first_name_ruby,
            last_name=user_dto.last_name,
            last_name_ruby=user_dto.last_name_ruby,
            gender=user_dto.gender,
            birth_day=user_dto.birth_day,
            phone_number=user_dto.phone_number,
            zip_code=user_dto.zip_code,
            address=user_dto.address,
            role_ids=[default_role_id],
            created_by="system",
            updated_by="system",
            delete_flag=0,
        )

        # ユーザーをリポジトリに保存
        created_user = self.user_repository.create(user)

        # レスポンスDTOを作成して返す
        return UserResponseDTO(
            id=created_user.id,
            username=created_user.username,
            email=created_user.email,
            first_name=created_user.first_name,
            first_name_ruby=created_user.first_name_ruby,
            last_name=created_user.last_name,
            last_name_ruby=created_user.last_name_ruby,
            gender=created_user.gender,
            birth_day=created_user.birth_day,
            phone_number=created_user.phone_number,
            zip_code=created_user.zip_code,
            address=created_user.address,
            role_ids=created_user.role_ids,
            created_at=created_user.created_at,
            created_by=created_user.created_by,
            updated_at=created_user.updated_at,
            updated_by=created_user.updated_by,
            delete_flag=created_user.delete_flag,
        )

    def _get_password_hash(self, password: str) -> str:
        """パスワードをハッシュ化する

        プレーンテキストのパスワードをbcryptを使用してハッシュ化します。

        Args:
            password (str): ハッシュ化する平文パスワード

        Returns:
            str: ハッシュ化されたパスワード
        """
        return pwd_context.hash(password)
