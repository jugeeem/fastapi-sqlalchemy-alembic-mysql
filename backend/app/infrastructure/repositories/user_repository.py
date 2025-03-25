from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId
from app.infrastructure.models.user import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, user_id: UserId) -> Optional[User]:
        user = self.db.query(UserModel).filter(UserModel.id == str(user_id)).first()
        if not user:
            return None

        return self._to_entity(user)

    def find_by_email(self, email: Email) -> Optional[User]:
        user = self.db.query(UserModel).filter(UserModel.email == str(email)).first()
        if not user:
            return None

        return self._to_entity(user)

    def find_all(self) -> List[User]:
        users = self.db.query(UserModel).all()
        return [self._to_entity(user) for user in users]

    def save(self, user: User) -> User:
        db_user = self.db.query(UserModel).filter(UserModel.id == str(user.id)).first()

        if not db_user:
            db_user = UserModel(
                id=str(user.id),
                email=str(user.email),
                name=user.name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            self.db.add(db_user)
        else:
            db_user.email = str(user.email)
            db_user.name = user.name
            db_user.is_active = user.is_active
            db_user.updated_at = datetime.now()

        self.db.commit()
        self.db.refresh(db_user)

        return self._to_entity(db_user)

    def delete(self, user_id: UserId) -> None:
        db_user = self.db.query(UserModel).filter(UserModel.id == str(user_id)).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=UserId(model.id),
            email=Email(model.email),
            name=model.name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
