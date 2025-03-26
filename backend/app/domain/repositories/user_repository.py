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
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: UserId) -> None:
        pass
