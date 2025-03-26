from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Optional

from app.domain.value_objects.attendance_id import AttendanceId
from app.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class Attendance:
    id: AttendanceId
    work_date: date  # dateからwork_dateに変更
    clock_in: time
    clock_out: time
    rest_in: time
    rest_out: time
    user_id: UserId
    remarks: Optional[str]
    work_place: Optional[str]
    transportation_expenses: Optional[int]
    delete_flag: bool
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str

    def calculate_working_hours(self) -> float:
        """労働時間を計算して返す（休憩時間を除く）"""
        # 労働時間の計算（秒に変換して差分を取る）
        work_seconds = self._time_to_seconds(
            self.clock_out
        ) - self._time_to_seconds(self.clock_in)

        # 休憩時間の計算
        rest_seconds = self._time_to_seconds(
            self.rest_out
        ) - self._time_to_seconds(self.rest_in)

        # 労働時間から休憩時間を引く
        total_seconds = work_seconds - rest_seconds

        # 時間に変換（小数点以下2桁まで）
        return round(total_seconds / 3600, 2)

    def calculate_rest_hours(self) -> float:
        """休憩時間を計算して返す"""
        rest_seconds = self._time_to_seconds(
            self.rest_out
        ) - self._time_to_seconds(self.rest_in)
        return round(rest_seconds / 3600, 2)

    def _time_to_seconds(self, t: time) -> int:
        """時間を秒に変換"""
        return t.hour * 3600 + t.minute * 60 + t.second

    def update(
        self,
        work_date: Optional[date] = None,  # dateからwork_dateに変更
        clock_in: Optional[time] = None,
        clock_out: Optional[time] = None,
        rest_in: Optional[time] = None,
        rest_out: Optional[time] = None,
        work_place: Optional[str] = None,
        transportation_expenses: Optional[int] = None,
        remarks: Optional[str] = None,
        updated_by: str = "",
    ) -> "Attendance":
        """勤怠情報を更新した新しいインスタンスを返す"""
        return Attendance(
            id=self.id,
            work_date=work_date
            if work_date is not None
            else self.work_date,  # 変更
            clock_in=clock_in if clock_in is not None else self.clock_in,
            clock_out=clock_out if clock_out is not None else self.clock_out,
            rest_in=rest_in if rest_in is not None else self.rest_in,
            rest_out=rest_out if rest_out is not None else self.rest_out,
            user_id=self.user_id,
            work_place=work_place
            if work_place is not None
            else self.work_place,
            transportation_expenses=transportation_expenses
            if transportation_expenses is not None
            else self.transportation_expenses,
            remarks=remarks if remarks is not None else self.remarks,
            delete_flag=self.delete_flag,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=datetime.now(),
            updated_by=updated_by if updated_by else self.updated_by,
        )

    def deactivate(self) -> "Attendance":
        """論理削除状態にした新しいインスタンスを返す"""
        if self.delete_flag:
            return self

        return Attendance(
            id=self.id,
            work_date=self.work_date,  # 変更
            clock_in=self.clock_in,
            clock_out=self.clock_out,
            rest_in=self.rest_in,
            rest_out=self.rest_out,
            user_id=self.user_id,
            work_place=self.work_place,
            transportation_expenses=self.transportation_expenses,
            remarks=self.remarks,
            delete_flag=True,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=datetime.now(),
            updated_by=self.updated_by,
        )

    def activate(self) -> "Attendance":
        """論理削除を解除した新しいインスタンスを返す"""
        if not self.delete_flag:
            return self

        return Attendance(
            id=self.id,
            work_date=self.work_date,  # 変更
            clock_in=self.clock_in,
            clock_out=self.clock_out,
            rest_in=self.rest_in,
            rest_out=self.rest_out,
            user_id=self.user_id,
            work_place=self.work_place,
            transportation_expenses=self.transportation_expenses,
            remarks=self.remarks,
            delete_flag=False,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=datetime.now(),
            updated_by=self.updated_by,
        )
