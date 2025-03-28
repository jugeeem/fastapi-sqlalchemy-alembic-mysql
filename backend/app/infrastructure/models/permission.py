from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.infrastructure.models.base_model import BaseModel


class PermissionModel(BaseModel):
    """システム内の操作権限を管理するテーブル"""
    __tablename__ = "permissions"

    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    resource = Column(String(255), nullable=False)  # 操作対象のリソース
    action = Column(String(50), nullable=False)  # 操作種別（create, read, update, delete等）
    
    # リレーションシップ
    roles = relationship("RolePermissionModel", back_populates="permission")
