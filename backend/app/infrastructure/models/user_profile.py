from datetime import date
from sqlalchemy import Column, String, Date, ForeignKey, Enum
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

from app.domain.value_objects.enums import Gender
from app.infrastructure.models.base_model import BaseModel


class UserProfileModel(BaseModel):
    """ユーザーの個人プロフィール情報を管理するテーブル"""
    __tablename__ = "user_profiles"

    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    first_name = Column(String(255), nullable=True)
    first_name_ruby = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    last_name_ruby = Column(String(255), nullable=True)
    gender = Column(Enum(Gender), nullable=False)
    birth_day = Column(Date, nullable=False)

    # リレーションシップ
    user = relationship("UserModel", back_populates="profile")
