from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from app.domain.entities.attendance import Attendance
from app.domain.value_objects.attendance_id import AttendanceId
from app.domain.value_objects.user_id import UserId


class AttendanceRepository(ABC):
    @abstractmethod
    def find_by_id(self, attendance_id: AttendanceId) -> Optional[Attendance]:
        """IDで勤怠情報を検索"""
        pass

    @abstractmethod
    def find_by_user_id_and_date(
        self,
        user_id: UserId,
        work_date: date,
    ) -> Optional[Attendance]:
        """ユーザーIDと日付で勤怠情報を検索"""
        pass

    @abstractmethod
    def find_by_user_id(
        self,
        user_id: UserId,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Attendance]:
        """ユーザーIDで勤怠情報を検索"""
        pass

    @abstractmethod
    def find_by_date_range(
        self,
        start_date: date,
        end_date: date,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Attendance]:
        """日付範囲で勤怠情報を検索"""
        pass

    @abstractmethod
    def find_by_user_id_and_date_range(
        self,
        user_id: UserId,
        start_date: date,
        end_date: date,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Attendance]:
        """ユーザーIDと日付範囲で勤怠情報を検索"""
        pass

    @abstractmethod
    def find_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        asc: bool = True,
    ) -> List[Attendance]:
        """全ての勤怠情報を検索"""
        pass

    @abstractmethod
    def save(self, attendance: Attendance) -> Attendance:
        """勤怠情報を保存"""
        pass

    @abstractmethod
    def delete(self, attendance_id: AttendanceId) -> None:
        """勤怠情報を削除（論理削除）"""
        pass
