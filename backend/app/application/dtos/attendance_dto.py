from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel, Field


class AttendanceCreateDTO(BaseModel):
    work_date: date  # dateからwork_dateに変更
    clock_in: time
    clock_out: time
    rest_in: time
    rest_out: time
    user_id: str
    work_place: Optional[str] = None
    transportation_expenses: Optional[int] = Field(None, ge=0)
    remarks: Optional[str] = None
    created_by: str
    updated_by: str


class AttendanceUpdateDTO(BaseModel):
    work_date: Optional[date] = None  # dateからwork_dateに変更
    clock_in: Optional[time] = None
    clock_out: Optional[time] = None
    rest_in: Optional[time] = None
    rest_out: Optional[time] = None
    work_place: Optional[str] = None
    transportation_expenses: Optional[int] = Field(None, ge=0)
    remarks: Optional[str] = None
    updated_by: str


class AttendanceResponseDTO(BaseModel):
    id: str
    work_date: date  # dateからwork_dateに変更
    clock_in: time
    clock_out: time
    rest_in: time
    rest_out: time
    user_id: str
    work_place: Optional[str] = None
    transportation_expenses: Optional[int] = None
    remarks: Optional[str] = None
    working_hours: float
    rest_hours: float
    delete_flag: bool
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str


class AttendanceQueryDTO(BaseModel):
    user_id: Optional[str] = None
    start_date: Optional[date] = (
        None  # このプロパティ名はクエリパラメータとして使うため変更しない
    )
    end_date: Optional[date] = (
        None  # このプロパティ名はクエリパラメータとして使うため変更しない
    )
    limit: Optional[int] = None
    offset: Optional[int] = None
    order_by: Optional[str] = None
    asc: bool = True
