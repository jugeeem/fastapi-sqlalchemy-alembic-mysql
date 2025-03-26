import uuid

from sqlalchemy import Column, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.mysql import CHAR

from app.infrastructure.models.base_model import BaseModel


class UserRoleModel(BaseModel):
    __tablename__ = "user_roles"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    role_id = Column(CHAR(36), ForeignKey("roles.id"), nullable=False)

    __table_args__ = (
        Index("idx_id", "id"),
        Index("idx_user_id", "user_id"),
        Index("idx_role_id", "role_id"),
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )
