# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ユーザーリポジトリインターフェースモジュール

このモジュールでは、ユーザーエンティティのデータアクセスを抽象化するリポジトリインターフェースを定義します。
このインターフェースによって、ドメイン層はデータの永続化メカニズムから分離され、依存性逆転の原則が適用されます。
"""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.entities.user import User


class UserRepository(ABC):
    """ユーザーリポジトリのインターフェース

    ユーザーエンティティの永続化と取得を担当するリポジトリの抽象基底クラスです。
    具体的な実装はインフラストラクチャ層で提供され、このインターフェースに従います。
    """

    @abstractmethod
    def create(self, user: User) -> User:
        """新規ユーザーを作成する

        ユーザーエンティティを受け取り、それを永続化します。
        作成後のエンティティ（IDなどが設定された状態）を返します。

        Args:
            user (User): 作成するユーザーエンティティ

        Returns:
            User: 作成されたユーザーエンティティ
        """
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """ユーザー名でユーザーを検索する

        指定されたユーザー名に一致するユーザーを検索します。

        Args:
            username (str): 検索するユーザー名

        Returns:
            Optional[User]: 見つかったユーザーエンティティ。見つからない場合はNone。
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """メールアドレスでユーザーを検索する

        指定されたメールアドレスに一致するユーザーを検索します。

        Args:
            email (str): 検索するメールアドレス

        Returns:
            Optional[User]: 見つかったユーザーエンティティ。見つからない場合はNone。
        """
        pass

    @abstractmethod
    def get_default_user_role_id(self) -> UUID:
        """デフォルトのユーザー権限IDを取得する

        システムのデフォルトユーザーロール（通常は一般ユーザーロール）のIDを取得します。
        新規ユーザー作成時のデフォルトロール割り当てに使用されます。

        Returns:
            UUID: デフォルトユーザーロールのID

        Raises:
            ValueError: デフォルトユーザーロールが見つからない場合
        """
        pass

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[User]:
        """ユーザーIDでユーザーを検索する

        指定されたユーザーIDに一致するユーザーを検索します。

        Args:
            user_id (UUID): 検索するユーザーID

        Returns:
            Optional[User]: 見つかったユーザーエンティティ。見つからない場合はNone。
        """
        pass

    @abstractmethod
    def get_users(
        self, offset: int = 0, limit: int = 100, ascending: bool = True
    ) -> list[User]:
        """ユーザー一覧を取得する

        ページネーションとソートに対応したユーザー一覧を取得します。

        Args:
            offset (int, optional): スキップするレコード数。デフォルトは0。
            limit (int, optional): 取得する最大レコード数。デフォルトは100。
            ascending (bool, optional): 昇順にソートするかどうか。デフォルトはTrue。

        Returns:
            list[User]: ユーザーエンティティのリスト
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """既存ユーザー情報を更新する

        ユーザーエンティティの情報を受け取り、データベースの対応するユーザー情報を更新します。
        更新されたエンティティを返します。

        Args:
            user (User): 更新するユーザー情報を含むエンティティ

        Returns:
            User: 更新されたユーザーエンティティ
        """
        pass

    @abstractmethod
    def remove(self, user_id: UUID, updated_by: str) -> None:
        """ユーザーを論理削除する

        指定されたユーザーIDに対応するユーザーを削除します。

        Args:
            user_id (UUID): 削除するユーザーのID
            updated_by (str): 更新者のユーザー名

        Raises:
            ValueError: ユーザーが見つからない場合
        """
        pass
