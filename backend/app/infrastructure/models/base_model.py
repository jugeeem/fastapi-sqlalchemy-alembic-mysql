import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import CHAR, TINYINT

from app.infrastructure.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    remarks = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    created_by = Column(String(255), nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    updated_by = Column(String(255), nullable=False)
    delete_flag = Column(TINYINT(1), default=0, nullable=False)
