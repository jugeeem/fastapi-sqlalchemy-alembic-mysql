import uuid

from sqlalchemy import Column, Date, ForeignKey, Index, Integer, String, Time
from sqlalchemy.dialects.mysql import CHAR

from app.infrastructure.models.base_model import BaseModel


class AttendanceModel(BaseModel):
    __tablename__ = "attendances"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    work_date = Column(Date, nullable=False)  # dateからwork_dateに変更
    clock_in = Column(Time, nullable=False)
    clock_out = Column(Time, nullable=False)
    rest_in = Column(Time, nullable=False)
    rest_out = Column(Time, nullable=False)
    work_place = Column(String(255), nullable=True)
    transportation_expenses = Column(Integer, nullable=True)
    user_id = Column(
        CHAR(36), ForeignKey("users.id"), nullable=False, index=True
    )

    __table_args__ = (
        Index("idx_id", "id"),
        Index("idx_user_date", "user_id", "work_date"),  # インデックス名も更新
        Index("idx_date", "work_date"),  # インデックス名も更新
    )
