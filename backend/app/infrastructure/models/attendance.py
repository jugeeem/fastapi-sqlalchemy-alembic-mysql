import enum
import uuid

from sqlalchemy import (
    Column,
    Date,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Time,
)
from sqlalchemy.dialects.mysql import CHAR

from app.infrastructure.models.base_model import BaseModel


class AttendanceStatusEnum(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELED = "CANCELED"


class AttendanceModel(BaseModel):
    __tablename__ = "attendances"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    work_date = Column(Date, nullable=False)
    clock_in = Column(Time, nullable=False)
    clock_out = Column(Time, nullable=False)
    rest_in = Column(Time, nullable=False)
    rest_out = Column(Time, nullable=False)
    work_place = Column(String(255), nullable=True)
    transportation_expenses = Column(Integer, nullable=True)
    status = Column(
        Enum(AttendanceStatusEnum),
        nullable=False,
        default=AttendanceStatusEnum.PENDING,
    )
    user_id = Column(
        CHAR(36), ForeignKey("users.id"), nullable=False, index=True
    )

    __table_args__ = (
        Index("idx_id", "id"),
        Index("idx_user_date", "user_id", "work_date"),
        Index("idx_date", "work_date"),
    )
