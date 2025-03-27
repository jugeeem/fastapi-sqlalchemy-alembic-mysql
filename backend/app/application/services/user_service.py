from datetime import datetime
from typing import List, Optional

from app.application.dtos.user_dto import (
    UserCreateDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: str) -> Optional[UserResponseDTO]:
        try:
            user_id_vo = UserId(user_id)
        except ValueError as err:
            raise ValueError(f"Invalid user ID: {user_id}") from err

        user = self.user_repository.find_by_id(user_id_vo)
        if not user:
            return None

        return UserResponseDTO(
            id=str(user.id),
            email=str(user.email),
            username=user.username,
            manager_id=user.manager_id,
            remarks=user.remarks,
            delete_flag=user.delete_flag,
            created_at=user.created_at,
            created_by=user.created_by,
            updated_at=user.updated_at,
            updated_by=user.updated_by,
            first_name=user.first_name,
            first_name_ruby=user.first_name_ruby,
            last_name=user.last_name,
            last_name_ruby=user.last_name_ruby,
            phone_number=user.phone_number,
            zip_code=user.zip_code,
            address=user.address,
        )

    def get_users(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        asc: bool = True,
    ) -> List[UserResponseDTO]:
        users = self.user_repository.find_all(
            limit=limit, offset=offset, order_by=order_by, asc=asc
        )
        return [
            UserResponseDTO(
                id=str(user.id),
                email=str(user.email),
                username=user.username,
                manager_id=user.manager_id,
                remarks=user.remarks,
                delete_flag=user.delete_flag,
                created_at=user.created_at,
                created_by=user.created_by,
                updated_at=user.updated_at,
                updated_by=user.updated_by,
                first_name=user.first_name,
                first_name_ruby=user.first_name_ruby,
                last_name=user.last_name,
                last_name_ruby=user.last_name_ruby,
                phone_number=user.phone_number,
                zip_code=user.zip_code,
                address=user.address,
            )
            for user in users
        ]

    def create_user(self, data: UserCreateDTO) -> UserResponseDTO:
        try:
            email = Email(data.email)
        except ValueError as e:
            raise ValueError(f"Invalid email: {str(e)}") from e

        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError(f"User with email {data.email} already exists")

        user = User(
            id=UserId.generate(),
            email=email,
            username=data.username,
            password=data.password,
            manager_id=data.manager_id,
            remarks=data.remarks,
            delete_flag=False,
            created_at=datetime.now(),
            created_by=data.created_by,
            updated_at=datetime.now(),
            updated_by=data.updated_by,
            first_name=data.first_name,
            first_name_ruby=data.first_name_ruby,
            last_name=data.last_name,
            last_name_ruby=data.last_name_ruby,
            phone_number=data.phone_number,
            zip_code=data.zip_code,
            address=data.address,
        )

        created_user = self.user_repository.create(user)

        return UserResponseDTO(
            id=str(created_user.id),
            email=str(created_user.email),
            username=created_user.username,
            manager_id=created_user.manager_id,
            remarks=created_user.remarks,
            delete_flag=created_user.delete_flag,
            created_at=created_user.created_at,
            created_by=created_user.created_by,
            updated_at=created_user.updated_at,
            updated_by=created_user.updated_by,
            first_name=created_user.first_name,
            first_name_ruby=created_user.first_name_ruby,
            last_name=created_user.last_name,
            last_name_ruby=created_user.last_name_ruby,
            phone_number=created_user.phone_number,
            zip_code=created_user.zip_code,
            address=created_user.address,
        )

    def update_user(
        self, user_id: str, data: UserUpdateDTO
    ) -> Optional[UserResponseDTO]:
        try:
            user_id_vo = UserId(user_id)
        except ValueError as err:
            raise ValueError(f"Invalid user ID: {user_id}") from err

        user = self.user_repository.find_by_id(user_id_vo)
        if not user:
            return None

        updated_user = user

        if data.username:
            updated_user = updated_user.update_username(data.username)

        if data.delete_flag is not None:
            if not data.delete_flag:
                updated_user = updated_user.activate()
            else:
                updated_user = updated_user.deactivate()

        updated_user = User(
            id=updated_user.id,
            email=updated_user.email,
            username=updated_user.username,
            password=data.password if data.password else updated_user.password,
            manager_id=data.manager_id
            if data.manager_id
            else updated_user.manager_id,
            remarks=data.remarks
            if data.remarks is not None
            else updated_user.remarks,
            delete_flag=updated_user.delete_flag,
            created_at=updated_user.created_at,
            created_by=updated_user.created_by,
            updated_at=datetime.now(),
            updated_by=data.updated_by,
            first_name=data.first_name
            if data.first_name is not None
            else updated_user.first_name,
            first_name_ruby=data.first_name_ruby
            if data.first_name_ruby is not None
            else updated_user.first_name_ruby,
            last_name=data.last_name
            if data.last_name is not None
            else updated_user.last_name,
            last_name_ruby=data.last_name_ruby
            if data.last_name_ruby is not None
            else updated_user.last_name_ruby,
            phone_number=data.phone_number
            if data.phone_number is not None
            else updated_user.phone_number,
            zip_code=data.zip_code
            if data.zip_code is not None
            else updated_user.zip_code,
            address=data.address
            if data.address is not None
            else updated_user.address,
        )

        saved_user = self.user_repository.update(updated_user)

        return UserResponseDTO(
            id=str(saved_user.id),
            email=str(saved_user.email),
            username=saved_user.username,
            manager_id=saved_user.manager_id,
            remarks=saved_user.remarks,
            delete_flag=saved_user.delete_flag,
            created_at=saved_user.created_at,
            created_by=saved_user.created_by,
            updated_at=saved_user.updated_at,
            updated_by=saved_user.updated_by,
            first_name=saved_user.first_name,
            first_name_ruby=saved_user.first_name_ruby,
            last_name=saved_user.last_name,
            last_name_ruby=saved_user.last_name_ruby,
            phone_number=saved_user.phone_number,
            zip_code=saved_user.zip_code,
            address=saved_user.address,
        )

    def delete_user(self, user_id: str) -> bool:
        try:
            user_id_vo = UserId(user_id)
        except ValueError as err:
            raise ValueError(f"Invalid user ID: {user_id}") from err

        user = self.user_repository.find_by_id(user_id_vo)
        if not user:
            return False

        self.user_repository.delete(user_id_vo)
        return True

    def promote_user_to_manager(self, user_id: str) -> Optional[UserResponseDTO]:
        """ユーザーの権限を'user'から'manager'に昇格させる。

        Args:
            user_id: 昇格させるユーザーの一意識別子。

        Returns:
            昇格させたユーザーの情報。見つからない場合はNone。

        Raises:
            ValueError: ユーザーIDが無効な場合。
        """
        try:
            user_id_vo = UserId(user_id)
        except ValueError as err:
            raise ValueError(f"Invalid user ID: {user_id}") from err

        promoted_user = self.user_repository.promote_to_manager(user_id_vo)
        if not promoted_user:
            return None

        return UserResponseDTO(
            id=str(promoted_user.id),
            email=str(promoted_user.email),
            username=promoted_user.username,
            manager_id=promoted_user.manager_id,
            remarks=promoted_user.remarks,
            delete_flag=promoted_user.delete_flag,
            created_at=promoted_user.created_at,
            created_by=promoted_user.created_by,
            updated_at=promoted_user.updated_at,
            updated_by=promoted_user.updated_by,
            first_name=promoted_user.first_name,
            first_name_ruby=promoted_user.first_name_ruby,
            last_name=promoted_user.last_name,
            last_name_ruby=promoted_user.last_name_ruby,
            phone_number=promoted_user.phone_number,
            zip_code=promoted_user.zip_code,
            address=promoted_user.address,
        )

    def promote_user_to_admin(self, user_id: str) -> Optional[UserResponseDTO]:
        """ユーザーの権限を'manager'から'admin'に昇格させる。

        Args:
            user_id: 昇格させるユーザーの一意識別子。

        Returns:
            昇格させたユーザーの情報。見つからないか現在の役割が'manager'でない場合はNone。

        Raises:
            ValueError: ユーザーIDが無効な場合。
        """
        try:
            user_id_vo = UserId(user_id)
        except ValueError as err:
            raise ValueError(f"Invalid user ID: {user_id}") from err

        promoted_user = self.user_repository.promote_to_admin(user_id_vo)
        if not promoted_user:
            return None

        return UserResponseDTO(
            id=str(promoted_user.id),
            email=str(promoted_user.email),
            username=promoted_user.username,
            manager_id=promoted_user.manager_id,
            remarks=promoted_user.remarks,
            delete_flag=promoted_user.delete_flag,
            created_at=promoted_user.created_at,
            created_by=promoted_user.created_by,
            updated_at=promoted_user.updated_at,
            updated_by=promoted_user.updated_by,
            first_name=promoted_user.first_name,
            first_name_ruby=promoted_user.first_name_ruby,
            last_name=promoted_user.last_name,
            last_name_ruby=promoted_user.last_name_ruby,
            phone_number=promoted_user.phone_number,
            zip_code=promoted_user.zip_code,
            address=promoted_user.address,
        )

    def demote_user_from_admin_to_manager(self, user_id: str) -> Optional[UserResponseDTO]:
        """ユーザーの権限を'admin'から'manager'に降格させる。

        Args:
            user_id: 降格させるユーザーの一意識別子。

        Returns:
            降格させたユーザーの情報。見つからないか現在の役割が'admin'でない場合はNone。

        Raises:
            ValueError: ユーザーIDが無効な場合。
        """
        try:
            user_id_vo = UserId(user_id)
        except ValueError as err:
            raise ValueError(f"Invalid user ID: {user_id}") from err

        demoted_user = self.user_repository.demote_from_admin_to_manager(user_id_vo)
        if not demoted_user:
            return None

        return UserResponseDTO(
            id=str(demoted_user.id),
            email=str(demoted_user.email),
            username=demoted_user.username,
            manager_id=demoted_user.manager_id,
            remarks=demoted_user.remarks,
            delete_flag=demoted_user.delete_flag,
            created_at=demoted_user.created_at,
            created_by=demoted_user.created_by,
            updated_at=demoted_user.updated_at,
            updated_by=demoted_user.updated_by,
            first_name=demoted_user.first_name,
            first_name_ruby=demoted_user.first_name_ruby,
            last_name=demoted_user.last_name,
            last_name_ruby=demoted_user.last_name_ruby,
            phone_number=demoted_user.phone_number,
            zip_code=demoted_user.zip_code,
            address=demoted_user.address,
        )
