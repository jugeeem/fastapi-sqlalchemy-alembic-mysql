import uuid

from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import CHAR

from app.domain.constants.roles import USER_ROLE, MANAGER_ROLE, ADMIN_ROLE, get_role_level
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

    # ドメイン層の定数を参照
    USER_ROLE = USER_ROLE
    MANAGER_ROLE = MANAGER_ROLE
    ADMIN_ROLE = ADMIN_ROLE

    @classmethod
    def get_role_level(cls, role_name):
        """ロールの権限レベルを取得する

        Args:
            role_name: ロール名

        Returns:
            権限レベル（値が大きいほど高い権限）
        """
        return get_role_level(role_name)
