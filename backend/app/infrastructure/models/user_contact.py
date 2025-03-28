from sqlalchemy import Column, String, ForeignKey, CheckConstraint
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

from app.infrastructure.models.base_model import BaseModel


class UserContactModel(BaseModel):
    """ユーザーの連絡先情報を管理するテーブル"""
    __tablename__ = "user_contacts"

    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    phone_number = Column(String(13), nullable=True)
    zip_code = Column(String(8), nullable=True)
    address = Column(String(255), nullable=True)

    # リレーションシップ
    user = relationship("UserModel", back_populates="contact")

    # 制約
    __table_args__ = (
        CheckConstraint(
            "phone_number IS NULL OR phone_number REGEXP '^[0-9]{3}-[0-9]{4}-[0-9]{4}$'",
            name="check_phone_format"
        ),
        CheckConstraint(
            "zip_code IS NULL OR zip_code REGEXP '^[0-9]{3}-[0-9]{4}$'",
            name="check_zipcode_format"
        ),
    )
