from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class User:
    id: UserId
    email: Email
    username: str
    password: str
    manager_id: str
    remarks: Optional[str]
    delete_flag: bool
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    first_name: Optional[str] = None
    first_name_ruby: Optional[str] = None
    last_name: Optional[str] = None
    last_name_ruby: Optional[str] = None
    phone_number: Optional[str] = None
    zip_code: Optional[str] = None
    address: Optional[str] = None

    def activate(self) -> "User":
        if not self.delete_flag:
            return self

        return User(
            id=self.id,
            email=self.email,
            username=self.username,
            password=self.password,
            manager_id=self.manager_id,
            remarks=self.remarks,
            delete_flag=False,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=datetime.now(),
            updated_by=self.updated_by,
            first_name=self.first_name,
            first_name_ruby=self.first_name_ruby,
            last_name=self.last_name,
            last_name_ruby=self.last_name_ruby,
            phone_number=self.phone_number,
            zip_code=self.zip_code,
            address=self.address,
        )

    def deactivate(self) -> "User":
        if self.delete_flag:
            return self

        return User(
            id=self.id,
            email=self.email,
            username=self.username,
            password=self.password,
            manager_id=self.manager_id,
            remarks=self.remarks,
            delete_flag=True,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=datetime.now(),
            updated_by=self.updated_by,
            first_name=self.first_name,
            first_name_ruby=self.first_name_ruby,
            last_name=self.last_name,
            last_name_ruby=self.last_name_ruby,
            phone_number=self.phone_number,
            zip_code=self.zip_code,
            address=self.address,
        )

    def update_username(self, username: str) -> "User":
        return User(
            id=self.id,
            email=self.email,
            username=username,
            password=self.password,
            manager_id=self.manager_id,
            remarks=self.remarks,
            delete_flag=self.delete_flag,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=datetime.now(),
            updated_by=self.updated_by,
            first_name=self.first_name,
            first_name_ruby=self.first_name_ruby,
            last_name=self.last_name,
            last_name_ruby=self.last_name_ruby,
            phone_number=self.phone_number,
            zip_code=self.zip_code,
            address=self.address,
        )
