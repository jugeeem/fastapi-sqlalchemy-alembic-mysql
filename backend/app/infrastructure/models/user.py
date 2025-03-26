import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import CHAR

from app.infrastructure.models.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    password = Column(String(255), nullable=False)
    manager_id = Column(CHAR(36), nullable=False)
