# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザーリポジトリ実装モジュール

このモジュールでは、ドメイン層で定義されたUserRepositoryインターフェースのSQLAlchemy実装を提供します。
データベースとのやり取りを担当し、ユーザーエンティティの永続化と取得を行います。
"""

from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.enums import Role
from app.infrastructure.models.role import RoleModel
from app.infrastructure.models.user import UserModel
from app.infrastructure.models.user_contact import UserContactModel
from app.infrastructure.models.user_profile import UserProfileModel
from app.infrastructure.models.user_role import UserRoleModel


class SQLAlchemyUserRepository(UserRepository):
    """UserRepositoryインターフェースのSQLAlchemy実装

    ユーザー関連のデータベース操作を行うクラスです。
    ドメインエンティティとデータベースモデルの変換を行い、
    ユーザーの作成、検索などの操作を提供します。

    Attributes:
        db_session (Session): SQLAlchemyデータベースセッション
    """

    def __init__(self, db_session: Session):
        """リポジトリの初期化

        Args:
            db_session (Session): SQLAlchemyデータベースセッション
        """
        self.db_session = db_session

    def create(self, user: User) -> User:
        """新規ユーザーをデータベースに作成する

        ユーザーエンティティを受け取り、関連するすべてのテーブル
        （users, user_profiles, user_contacts, user_roles）にデータを作成します。

        Args:
            user (User): 作成するユーザーエンティティ

        Returns:
            User: 作成されたユーザーエンティティ（IDや作成日時などが設定された状態）

        Raises:
            Exception: データベース操作中に発生した例外
        """
        try:
            # UserModelの作成
            user_id = uuid4()
            user_model = UserModel(
                id=user_id,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
                created_by="system",
                updated_by="system",
            )
            self.db_session.add(user_model)

            # UserProfileModelの作成
            profile_model = UserProfileModel(
                user_id=user_id,
                first_name=user.first_name,
                first_name_ruby=user.first_name_ruby,
                last_name=user.last_name,
                last_name_ruby=user.last_name_ruby,
                gender=user.gender,
                birth_day=user.birth_day,
                created_by=user_model.created_by,
                updated_by=user_model.updated_by,
            )
            self.db_session.add(profile_model)

            # UserContactModelの作成
            contact_model = UserContactModel(
                user_id=user_id,
                phone_number=user.phone_number,
                zip_code=user.zip_code,
                address=user.address,
                created_by=user_model.created_by,
                updated_by=user_model.updated_by,
            )
            self.db_session.add(contact_model)

            # UserRoleModelの作成
            for role_id in user.role_ids:
                role_model = UserRoleModel(
                    user_id=user_id,
                    role_id=role_id,
                    created_by=user_model.created_by,
                    updated_by=user_model.updated_by,
                )
                self.db_session.add(role_model)

            self.db_session.commit()
            self.db_session.refresh(user_model)

            # エンティティに変換して返す
            user.id = user_id
            user.created_at = user_model.created_at
            user.created_by = user_model.created_by
            user.updated_at = user_model.updated_at
            user.updated_by = user_model.updated_by
            return user
        except Exception as e:
            self.db_session.rollback()
            raise e

    def find_by_username(self, username: str) -> Optional[User]:
        """ユーザー名でユーザーを検索する

        指定されたユーザー名に一致するユーザーをデータベースから検索します。

        Args:
            username (str): 検索するユーザー名

        Returns:
            Optional[User]: 見つかったユーザーエンティティ。見つからない場合はNone。

        Raises:
            Exception: データベース操作中に発生した例外
        """
        try:
            user_model = (
                self.db_session.query(UserModel)
                .filter(UserModel.username == username)
                .first()
            )
            if not user_model:
                return None

            return self._model_to_entity(user_model)
        except Exception as e:
            self.db_session.rollback()
            raise e

    def find_by_email(self, email: str) -> Optional[User]:
        """メールアドレスでユーザーを検索する

        指定されたメールアドレスに一致するユーザーをデータベースから検索します。

        Args:
            email (str): 検索するメールアドレス

        Returns:
            Optional[User]: 見つかったユーザーエンティティ。見つからない場合はNone。

        Raises:
            Exception: データベース操作中に発生した例外
        """
        try:
            user_model = (
                self.db_session.query(UserModel)
                .filter(UserModel.email == email)
                .first()
            )
            if not user_model:
                return None

            return self._model_to_entity(user_model)
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_default_user_role_id(self) -> UUID:
        """デフォルトのユーザー権限IDを取得する

        ユーザー権限（USER）のIDをデータベースから検索して返します。
        新規ユーザー作成時のデフォルトロール割り当てに使用されます。

        Returns:
            UUID: デフォルトユーザーロールのID

        Raises:
            ValueError: デフォルトのユーザーロールがデータベースに存在しない場合
        """
        user_role = (
            self.db_session.query(RoleModel)
            .filter(RoleModel.name == Role.USER)
            .first()
        )
        if not user_role:
            raise ValueError("Default user role not found in database")
        return user_role.id

    def _model_to_entity(self, user_model: UserModel) -> User:
        """データベースモデルからドメインエンティティへの変換

        UserModelと関連するテーブルの情報からUserエンティティを作成します。

        Args:
            user_model (UserModel): 変換元のUserModelインスタンス

        Returns:
            User: 変換されたUserエンティティ
        """
        # RoleのIDリストを取得
        role_ids = [role.role_id for role in user_model.roles]

        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            first_name=user_model.profile.first_name
            if user_model.profile
            else None,
            first_name_ruby=user_model.profile.first_name_ruby
            if user_model.profile
            else None,
            last_name=user_model.profile.last_name
            if user_model.profile
            else None,
            last_name_ruby=user_model.profile.last_name_ruby
            if user_model.profile
            else None,
            gender=user_model.profile.gender if user_model.profile else None,
            birth_day=user_model.profile.birth_day
            if user_model.profile
            else None,
            phone_number=user_model.contact.phone_number
            if user_model.contact
            else None,
            zip_code=user_model.contact.zip_code
            if user_model.contact
            else None,
            address=user_model.contact.address if user_model.contact else None,
            role_ids=role_ids,
            created_at=user_model.created_at,
            created_by=user_model.created_by,
            updated_at=user_model.updated_at,
            updated_by=user_model.updated_by,
            delete_flag=user_model.delete_flag,
        )
