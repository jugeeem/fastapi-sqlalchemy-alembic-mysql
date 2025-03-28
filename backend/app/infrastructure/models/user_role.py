from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

from app.infrastructure.models.base_model import BaseModel


class UserRoleModel(BaseModel):
    """ユーザーとロールの関連を管理する中間テーブル"""
    __tablename__ = "user_roles"

    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    role_id = Column(CHAR(36), ForeignKey("roles.id"), nullable=False)
    
    # リレーションシップ
    user = relationship("UserModel", back_populates="roles")
    role = relationship("RoleModel", back_populates="users")
