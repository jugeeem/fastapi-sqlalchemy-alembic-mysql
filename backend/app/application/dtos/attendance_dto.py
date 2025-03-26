from datetime import date, datetime, time
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AttendanceStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELED = "CANCELED"


class AttendanceCreateDTO(BaseModel):
    work_date: date
    clock_in: time
    clock_out: time
    rest_in: time
    rest_out: time
    user_id: str
    status: AttendanceStatus = AttendanceStatus.PENDING
    work_place: Optional[str] = None
    transportation_expenses: Optional[int] = Field(None, ge=0)
    remarks: Optional[str] = None
    created_by: str
    updated_by: str


class AttendanceUpdateDTO(BaseModel):
    work_date: Optional[date] = None
    clock_in: Optional[time] = None
    clock_out: Optional[time] = None
    rest_in: Optional[time] = None
    rest_out: Optional[time] = None
    status: Optional[AttendanceStatus] = None
    work_place: Optional[str] = None
    transportation_expenses: Optional[int] = Field(None, ge=0)
    remarks: Optional[str] = None
    updated_by: str


class AttendanceResponseDTO(BaseModel):
    id: str
    work_date: date
    clock_in: time
    clock_out: time
    rest_in: time
    rest_out: time
    user_id: str
    status: AttendanceStatus
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
    status: Optional[AttendanceStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    order_by: Optional[str] = None
    asc: bool = True
