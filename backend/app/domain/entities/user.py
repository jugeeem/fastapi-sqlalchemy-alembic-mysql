from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class User:
    id: UserId
    email: Email
    name: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    def activate(self) -> "User":
        if self.is_active:
            return self

        return User(
            id=self.id,
            email=self.email,
            name=self.name,
            is_active=True,
            created_at=self.created_at,
            updated_at=datetime.now(),
        )

    def deactivate(self) -> "User":
        if not self.is_active:
            return self

        return User(
            id=self.id,
            email=self.email,
            name=self.name,
            is_active=False,
            created_at=self.created_at,
            updated_at=datetime.now(),
        )

    def update_name(self, name: str) -> "User":
        return User(
            id=self.id,
            email=self.email,
            name=name,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=datetime.now(),
        )
