import uuid

from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import CHAR

from app.infrastructure.models.base_model import BaseModel


class RoleModel(BaseModel):
    __tablename__ = "roles"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    role_name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

    __table_args__ = (
        Index("idx_id", "id"),
        Index("idx_role_name", "role_name"),
    )
