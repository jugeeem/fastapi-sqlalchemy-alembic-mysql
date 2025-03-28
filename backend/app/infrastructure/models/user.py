from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.domain.value_objects.enums import Gender
from app.infrastructure.models.base_model import BaseModel


class UserModel(BaseModel):
    """ユーザー認証情報を管理するテーブル"""
    __tablename__ = "users"

    # 認証情報
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # リレーションシップ
    profile = relationship("UserProfileModel", back_populates="user", uselist=False)
    contact = relationship("UserContactModel", back_populates="user", uselist=False)
    roles = relationship("UserRoleModel", back_populates="user")
