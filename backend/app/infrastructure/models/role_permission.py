from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

from app.infrastructure.models.base_model import BaseModel


class RolePermissionModel(BaseModel):
    """ロールと権限の関連を管理する中間テーブル"""
    __tablename__ = "role_permissions"

    role_id = Column(CHAR(36), ForeignKey("roles.id"), nullable=False)
    permission_id = Column(CHAR(36), ForeignKey("permissions.id"), nullable=False)
    
    # リレーションシップ
    role = relationship("RoleModel", back_populates="permissions")
    permission = relationship("PermissionModel", back_populates="roles")
