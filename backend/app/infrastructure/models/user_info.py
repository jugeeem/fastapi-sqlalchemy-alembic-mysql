from sqlalchemy import Column, ForeignKey, Index, String
from sqlalchemy.dialects.mysql import CHAR

from app.infrastructure.models.base_model import BaseModel


class UserInfoModel(BaseModel):
    __tablename__ = "user_info"

    user_id = Column(
        CHAR(36), ForeignKey("users.id"), nullable=False, index=True
    )
    first_name = Column(String(255), nullable=True)
    first_name_ruby = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    last_name_ruby = Column(String(255), nullable=True)
    phone_number = Column(String(13), nullable=True)
    zip_code = Column(String(8), nullable=True)
    address = Column(String(255), nullable=True)

    __table_args__ = (
        Index("idx_id", "id"),
        Index("idx_user_id", "user_id"),
    )
