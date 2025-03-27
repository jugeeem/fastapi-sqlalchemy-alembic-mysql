from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.user import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: UserId) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    def find_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        asc: bool = True,
    ) -> List[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        """新しいユーザーを作成する。

        Args:
            user: 作成するUserエンティティ。

        Returns:
            作成されたUserエンティティ。
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """既存のユーザーを更新する。

        Args:
            user: 更新するUserエンティティ。

        Returns:
            更新されたUserエンティティ。
        """
        pass

    @abstractmethod
    def delete(self, user_id: UserId) -> None:
        pass

    @abstractmethod
    def promote_to_manager(self, user_id: UserId) -> Optional[User]:
        """ユーザーの権限を'user'から'manager'に昇格させる。

        Args:
            user_id: 昇格させるユーザーの一意識別子。

        Returns:
            昇格させたユーザー。見つからない場合はNone。
        """
        pass

    @abstractmethod
    def promote_to_admin(self, user_id: UserId) -> Optional[User]:
        """ユーザーの権限を'manager'から'admin'に昇格させる。

        Args:
            user_id: 昇格させるユーザーの一意識別子。

        Returns:
            昇格させたユーザー。見つからないか現在の役割が'manager'でない場合はNone。
        """
        pass

    @abstractmethod
    def demote_from_admin_to_manager(self, user_id: UserId) -> Optional[User]:
        """ユーザーの権限を'admin'から'manager'に降格させる。

        Args:
            user_id: 降格させるユーザーの一意識別子。

        Returns:
            降格させたユーザー。見つからないか現在の役割が'admin'でない場合はNone。
        """
        pass

    @abstractmethod
    def demote_from_manager_to_user(self, user_id: UserId) -> Optional[User]:
        """ユーザーの権限を'manager'から'user'に降格させる。

        Args:
            user_id: 降格させるユーザーの一意識別子。

        Returns:
            降格させたユーザー。見つからないか現在の役割が'manager'でない場合はNone。
        """
        pass
