from datetime import datetime
from typing import List, Optional

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId
from app.application.dtos.user_dto import UserCreateDTO, UserUpdateDTO, UserResponseDTO


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: str) -> Optional[UserResponseDTO]:
        try:
            user_id_vo = UserId(user_id)
        except ValueError:
            raise ValueError(f"Invalid user ID: {user_id}")

        user = self.user_repository.find_by_id(user_id_vo)
        if not user:
            return None

        return UserResponseDTO(
            id=str(user.id),
            email=str(user.email),
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def get_users(self) -> List[UserResponseDTO]:
        users = self.user_repository.find_all()
        return [
            UserResponseDTO(
                id=str(user.id),
                email=str(user.email),
                name=user.name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ]

    def create_user(self, data: UserCreateDTO) -> UserResponseDTO:
        try:
            email = Email(data.email)
        except ValueError as e:
            raise ValueError(f"Invalid email: {str(e)}")

        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError(f"User with email {data.email} already exists")

        user = User(
            id=UserId.generate(),
            email=email,
            name=data.name,
            is_active=True,
            created_at=datetime.now(),
        )

        created_user = self.user_repository.save(user)

        return UserResponseDTO(
            id=str(created_user.id),
            email=str(created_user.email),
            name=created_user.name,
            is_active=created_user.is_active,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at,
        )

    def update_user(
        self, user_id: str, data: UserUpdateDTO
    ) -> Optional[UserResponseDTO]:
        try:
            user_id_vo = UserId(user_id)
        except ValueError:
            raise ValueError(f"Invalid user ID: {user_id}")

        user = self.user_repository.find_by_id(user_id_vo)
        if not user:
            return None

        if data.name:
            user = user.update_name(data.name)

        if data.is_active is not None:
            if data.is_active:
                user = user.activate()
            else:
                user = user.deactivate()

        updated_user = self.user_repository.save(user)

        return UserResponseDTO(
            id=str(updated_user.id),
            email=str(updated_user.email),
            name=updated_user.name,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
        )

    def delete_user(self, user_id: str) -> bool:
        try:
            user_id_vo = UserId(user_id)
        except ValueError:
            raise ValueError(f"Invalid user ID: {user_id}")

        user = self.user_repository.find_by_id(user_id_vo)
        if not user:
            return False

        self.user_repository.delete(user_id_vo)
        return True
