from sqlalchemy import Column, String, Enum, Text
from sqlalchemy.orm import relationship

from app.domain.value_objects.enums import Role
from app.infrastructure.models.base_model import BaseModel


class RoleModel(BaseModel):
    """ユーザーロールを管理するテーブル"""
    __tablename__ = "roles"

    name = Column(Enum(Role), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # リレーションシップ
    users = relationship("UserRoleModel", back_populates="role")
    permissions = relationship("RolePermissionModel", back_populates="role")
